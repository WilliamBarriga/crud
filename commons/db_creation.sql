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