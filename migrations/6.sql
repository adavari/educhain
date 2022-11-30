create table error_request
(
	id uuid default uuid_generate_v4()
		constraint error_request_pk
			primary key,
	url varchar(255) not null,
	method varchar(10) not null,
	body jsonb,
	headers jsonb,
	status int default 0 not null,
	created_at timestamp default now(),
	updated_at timestamp default now()
);
