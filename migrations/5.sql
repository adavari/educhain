create table topic
(
	id uuid default uuid_generate_v4()
		constraint topic_pk
			primary key,
	question varchar(255) not null,
	default_answer text,
	course_id uuid not null
		constraint topic_course_id_fk
			references course
				on update cascade on delete cascade,
	created_at timestamp default now(),
	updated_at timestamp default now()
);

alter table faqs
	add course_id uuid;

alter table faqs
	add constraint faqs_course_id_fk
		foreign key (course_id) references course
			on update cascade on delete cascade;

alter table message
	add course_id uuid;

alter table message
	add constraint message_course_id_fk
		foreign key (course_id) references course
			on update cascade on delete cascade;

