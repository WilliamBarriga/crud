-- tables --

create or replace function trigger_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at=now();
    return new;
end;
$$;

create table if not exists users(
    id bigserial primary key,
    name varchar not null,
    email varchar not null unique,
    password varchar not null,
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now(),
    active boolean not null default true
);

drop trigger if exists set_users_updated_at on users;

create trigger set_users_updated_at
before update on users
for each row execute procedure trigger_updated_at();

create table if not exists categories(
    id bigserial primary key,
    name varchar not null,
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now(),
    active boolean not null default true
);

drop trigger if exists set_categories_updated_at on categories;

create trigger set_categories_updated_at
before update on categories
for each row execute procedure trigger_updated_at();

create table if not exists books(
    id bigserial primary key,
    name varchar not null,
    author varchar,
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now(),
    active boolean not null default true
);

drop trigger if exists set_books_updated_at on books;

create trigger set_books_updated_at
before update on books
for each row execute procedure trigger_updated_at();

create table if not exists books_categories(
    id bigserial primary key,
    book_id bigint not null,
    category_id bigint not null,
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now(),
    active boolean not null default true
);

alter table books_categories drop constraint if exists books_categories_book_id_fk;
alter table books_categories drop constraint if exists books_categories_category_id_fk;
alter table books_categories add constraint books_categories_book_id_fk foreign key (book_id) references books (id);
alter table books_categories add constraint books_categories_category_id_fk foreign key (category_id) references categories (id);

drop trigger if exists set_books_categories_updated_at on books_categories;

create trigger set_books_categories_updated_at 
before update on books_categories
for each row execute procedure trigger_updated_at();

create table if not exists likes(
    id bigserial primary key,
    user_id bigint not null,
    book_id bigint not null,
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now(),
    active boolean not null default true
);

alter table likes drop constraint if exists likes_book_id_fk;
alter table likes drop constraint if exists likes_user_id_fk;
alter table likes add constraint likes_book_id_fk foreign key (book_id) references books (id);
alter table likes add constraint likes_user_id_fk foreign key (user_id) references users (id);

drop trigger if exists set_likes_updated_at on likes;

create trigger set_likes_updated_at
before update on likes
for each row execute procedure trigger_updated_at();

-- functions --

drop function if exists crud_validate_user_mail;

create or replace function crud_validate_user_mail(
    _email varchar,
    out duplicated bool
)
language plpgsql
as $$
    begin
    if exists (select from users u where u.email = _email) 
    then duplicated := true;
   end if;
   end;

$$;

--
drop function if exists crud_create_user;

create or replace function crud_create_user(
    _name varchar,
    _email varchar,
    _password varchar
)
returns setof users
language plpgsql
as $$
    begin
    return query
        insert into users("name", email, "password")
        values(_name, _email, _password)
        returning *;
   end;

$$;

--
drop function if exists crud_auth_user;

create or replace function crud_auth_user(
    _email varchar
)
returns setof users
language plpgsql
as $$
    begin
    return query
        select *
        from users u
        where u.email = _email;
   end;

$$;

--
drop function if exists crud_create_category;

create or replace function crud_create_category(
    _name varchar
)
returns setof categories
language plpgsql
as $$
    begin
    return query
        insert into categories("name")
        values (_name)
        returning *;
   end;

$$;

--

drop function if exists crud_get_categories;

create or replace function crud_get_categories(
    _q varchar
)
returns table(id bigint, name varchar, active bool)
language plpgsql
as $$
    begin
    return query
        select c.id, c."name", c.active
        from categories c
        where c.active = true
        and  case when _q is not null 
            then c."name" ilike '%' || _q || '%'
            else true
        end
        order by created_at desc;
   end;

$$;

--
drop function if exists crud_delete_categories;

create or replace function crud_delete_categories(
    _id bigint
)
returns setof categories
language plpgsql
as $$
    begin
    return query
        update categories 
        set active = not active
        where id = _id
        returning *;
   end;

$$;

---
drop function if exists crud_get_books;

create or replace function crud_get_books(
    _q varchar,
    _categories int[],
    _b_id bigint[],
    _u_id bigint
)
returns table (id bigint, name varchar, author varchar, updated_at timestamptz, active bool, categories jsonb)
language plpgsql
as $$
    begin
    return query
        select b.id, b."name", b.author, b.updated_at, b.active,
		jsonb_agg(
			jsonb_build_object(
				'id', c.id,
				'name', c."name",
				'active', bc.active
			) order by c."name"
		) 
		from books b
		left join books_categories bc on b.id = bc.book_id 
		left join categories c on bc.category_id = c.id and c.active = true
		left join likes l on l.book_id = b.id
        where b.active = true
		and case when _b_id is not null
			then b.id = any(_b_id) 
			else true
		and case when _q is not null 
			then b."name" ilike '%' || _q || '%' or b.author ilike '%' || _q || '%'
			else true
		end
		end
		and case when _categories is not null 
			then c.id = any(_categories)
			else true
		end
        and case when _u_id is not null
            then l.user_id = _u_id
            else true
        end
		group by b.id;

   end;

$$;


--
drop function if exists crud_create_books;

create or replace function crud_create_books(
    _name varchar,
    _author varchar,
    _categories int[]
)
returns table (id bigint, name varchar, author varchar, updated_at timestamptz, active bool, categories jsonb)
language plpgsql
as $$
	declare
		_b_id bigint;
    begin
	    insert into books("name", author)
	    values (_name, _author)
	    returning books.id into _b_id;
	    
	   	insert into books_categories(book_id, category_id)
	   	select _b_id, unnest(_categories);
	   
    return query
        select * from crud_get_books(null::varchar, null::int[], array[_b_id]::bigint[], null::bigint);
   end;

$$;

--
drop function if exists crud_update_books;

create or replace function crud_update_books(
	_b_id bigint,
    _name varchar,
    _author varchar,
    _categories int[]
)
returns table (id bigint, name varchar, author varchar, updated_at timestamptz, active bool, categories jsonb)
language plpgsql
as $$
	declare
		_c record;
    begin
	    update books
	    set 
	    	"name"=coalesce(_name, books."name"),
	    	author=coalesce(_author, books.author)
	    where books.id = _b_id;
	   
	   	update books_categories 
	   		set active = false
	   	where book_id = _b_id;
	   
	   	for _c in 
	   		select unnest(_categories) cat
	   	loop
		   	if exists (
		   		select 1
		   		from books_categories bc 
		   		where bc.book_id = _b_id
		   			and bc.category_id = _c.cat
		   	) then
		   		update books_categories 
		   			set active = true
		   			where book_id = _b_id and category_id = _c.cat;
		   	else
   			   	insert into books_categories(book_id, category_id)
				values(_b_id, _c.cat);
			end if;
	   		
	   	end loop;

    return query
        select * from crud_get_books(null::varchar, null::int[], array[_b_id]::bigint[], null::bigint);
   end;

$$;

--
drop function if exists crud_delete_books;

create or replace function crud_delete_books(
	_b_id bigint
)
returns void
language plpgsql
as $$
    begin
	    update books
	    set 
	    	active = false
	    where books.id = _b_id;
	   
	   	update books_categories 
	   		set active = false
	   	where book_id = _b_id;
	   
   end;

$$;

--
drop function if exists crud_like_books;

create or replace function crud_like_books(
	_b_id bigint,
	_u_id bigint
)
returns table (id bigint, name varchar, author varchar, updated_at timestamptz, active bool, categories jsonb)
language plpgsql
as $$
	begin
	    if exists (
	    	select 1
	    	from likes l
	    	where l.book_id = _b_id and l.user_id = _u_id
	    ) then
	    	update likes
	    		set active = not active
	    	where l.book_id = _b_id and l.user_id = _u_id;
	    else
	    	insert into likes(book_id, user_id)
	    	values(_b_id, _u_id);
	   	end if;
		return query
        select * from crud_get_books(null::varchar, null::int[], array[_b_id]::bigint[], null::bigint);
	end;

$$;

---

drop function if exists crud_user_like_books;

create or replace function crud_user_like_books(
	_u_id bigint
)
returns table (
	principal_categories jsonb,
	books jsonb,
	total_books bigint
)
language plpgsql
as $$
	begin
	
	return query
		select 
			jsonb_agg(
				jsonb_build_object(
					'id', pc.id,
					'name', pc.name,
					'books', pc.books
				) order by pc.books
			) principal_categories,
			jsonb_agg(
				jsonb_build_object(
					'id', ub.id,
					'name', ub.name,
					'author', ub.author,
					'categories', ub.categories
				) order by pc.books
			) books, 
			count(distinct l.id) 
		from likes l 
		left join books b on b.id  = l.book_id 
		left join books_categories bc on b.id = bc.book_id and bc.active = true
		left join (
			select c.id, c.name, count(distinct bc.book_id) books
			from categories c
			join books_categories bc on c.id = bc.category_id 
			group by c.id
		) pc on bc.category_id = pc.id
		left join (
			select * from crud_get_books(null::varchar, null::int[], null::bigint[], _u_id)
		) ub on true
		where l.user_id = _u_id
		group by l.user_id;
	end;

$$;