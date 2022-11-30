create table app
(
	id uuid default uuid_generate_v4()
		constraint app_pk
			primary key,
	version_code int not null,
	created_at timestamp default now(),
	updated_at timestamp default now()
);

create table distribution_app
(
	id uuid default uuid_generate_v4()
		constraint distribution_app_pk
			primary key,
	distribution_id uuid not null
		constraint distribution_app_distribution_id_fk
			references distribution
				on update cascade on delete cascade,
	app_id uuid not null
		constraint distribution_app_app_id_fk
			references app
				on update cascade on delete cascade,
	status int default 0 not null,
	link varchar(255),
	created_at timestamp default now(),
	updated_at timestamp default now()
);

