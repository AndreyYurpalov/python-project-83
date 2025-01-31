CREATE TABLE IF NOT EXISTS public.urls
(
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name character varying(255) NOT NULL,
    created_at date NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS public.url_checks
(
    id bigint NOT NULL,
    url_id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    status_code smallint,
    h1 text,
    title text,
    description text,
    created_at date NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT url_checks_pkey PRIMARY KEY (url_id),
    CONSTRAINT id FOREIGN KEY (id)
        REFERENCES public.urls (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);


TRUNCATE public.urls, public.url_checks RESTART IDENTITY;
