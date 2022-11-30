create table notification
(
	id uuid default uuid_generate_v4(),
	title varchar(255) not null,
	body varchar(500) not null,
	push_type int default 1 not null,
	status int default 0,
	firebase_token varchar(255),
	result_log jsonb,
	created_at timestamp default now(),
	updated_at timestamp default now()
);