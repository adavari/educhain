create table admin_user
(
	id uuid default uuid_generate_v4()
		constraint admin_user_pk
			primary key,
	username varchar(255) not null,
	password varchar(255) not null,
	last_login timestamp,
	created_at timestamp default now(),
	updated_at timestamp default now()
);

create unique index admin_user_username_uindex
	on admin_user (username);

alter table course
	add teacher varchar(255) not null;

