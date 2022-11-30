create table analytics
(
	id uuid default uuid_generate_v4()
		constraint analytics_pk
			primary key,
	keyword uuid not null
		constraint analytics_keyword_distribution_fk
			references distribution
				on update cascade on delete cascade,
	analytics_type int default 1,
	created_at timestamp default now(),
	updated_at timestamp default now()
);

alter table distribution
	add installed bigint default 0;