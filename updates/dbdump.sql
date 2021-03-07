--
-- PostgreSQL database dump
--

-- Dumped from database version 11.7 (Debian 11.7-0+deb10u1)
-- Dumped by pg_dump version 11.7 (Debian 11.7-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: service; Type: TABLE; Schema: public; Owner: signout
--

CREATE TABLE public.service (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    type character varying(8)
);


ALTER TABLE public.service OWNER TO signout;

--
-- Name: service_id_seq; Type: SEQUENCE; Schema: public; Owner: signout
--

CREATE SEQUENCE public.service_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.service_id_seq OWNER TO signout;

--
-- Name: service_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: signout
--

ALTER SEQUENCE public.service_id_seq OWNED BY public.service.id;


--
-- Name: signout; Type: TABLE; Schema: public; Owner: signout
--

CREATE TABLE public.signout (
    id integer NOT NULL,
    intern_name character varying(64) NOT NULL,
    intern_callback character varying(16) NOT NULL,
    service integer NOT NULL,
    oncall boolean DEFAULT false NOT NULL,
    active boolean DEFAULT true NOT NULL,
    addtime timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completetime timestamp without time zone
);


ALTER TABLE public.signout OWNER TO signout;

--
-- Name: signout_id_seq; Type: SEQUENCE; Schema: public; Owner: signout
--

CREATE SEQUENCE public.signout_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.signout_id_seq OWNER TO signout;

--
-- Name: signout_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: signout
--

ALTER SEQUENCE public.signout_id_seq OWNED BY public.signout.id;


--
-- Name: service id; Type: DEFAULT; Schema: public; Owner: signout
--

ALTER TABLE ONLY public.service ALTER COLUMN id SET DEFAULT nextval('public.service_id_seq'::regclass);


--
-- Name: signout id; Type: DEFAULT; Schema: public; Owner: signout
--

ALTER TABLE ONLY public.signout ALTER COLUMN id SET DEFAULT nextval('public.signout_id_seq'::regclass);


--
-- Data for Name: service; Type: TABLE DATA; Schema: public; Owner: signout
--

COPY public.service (id, name, type) FROM stdin;
1	Breast, Intern #1	NF9132
2	Breast, Intern #2	NF9132
3	Breast, Sub-Intern	NF9132
4	Breast, APP	NF9132
5	GI A, Intern #1	NF9132
6	GI A, Intern #2	NF9132
7	GI A, Intern #3	NF9132
8	GI B, Intern #1	NF9132
9	GI B, Intern #2	NF9132
10	GI B, Intern #3	NF9132
11	GI B, Sub-Intern	NF9132
12	STR, Intern #1	NF9133
13	STR, Intern #2	NF9133
14	STR, Sub-Intern #1	NF9133
15	STR, NP	NF9133
16	Gen Med, Intern #1	NF9133
17	Gen Med, Intern #2	NF9133
18	Gen Med, Intern #3	NF9133
19	Leukemia A, Intern #1	NF9133
20	Leukemia A, Intern #2	NF9133
21	Leukemia A, Intern #3	NF9133
22	Leukemia A, NP	NF9133
23	Leukemia A, Sub-Intern	NF9133
24	Leukemia B, Intern #1	NF9133
25	Leukemia B, Intern #2	NF9133
26	Leukemia B, NP	NF9133
27	Leukemia B, Sub-Intern	NF9133
28	Lymphoma Green, Intern #1	NF9133
29	Lymphoma Green, Intern #2	NF9133
30	Lymphoma Green, Intern #3	NF9133
31	Lymphoma Green, Intern #3	NF9133
32	Lymphoma Green, Sub-Intern	NF9133
\.


--
-- Data for Name: signout; Type: TABLE DATA; Schema: public; Owner: signout
--

COPY public.signout (id, intern_name, intern_callback, service, oncall, active, addtime, completetime) FROM stdin;
5	Arlie Ditzler	x4850	10	f	t	2020-10-04 20:14:32.480771	2020-10-04 20:18:44.835648
2	Gwenn Arnold	x6152	28	f	t	2020-10-04 20:19:29.478708	2020-10-04 20:23:44.835648
6	Nancie Hogg	x9323	14	f	t	2020-10-04 20:22:29.481326	2020-10-04 20:33:44.835648
10	Ola Torres	x9420	29	f	t	2020-10-04 20:25:01.483296	2020-10-04 20:48:44.835648
4	Carl Silverberg	x5970	8	f	t	2020-10-04 20:27:23.480083	2020-10-04 22:33:44.835648
11	Gearldine Foxworth	x1100	30	f	t	2020-10-04 20:39:24.483929	2020-10-04 22:35:14.835648
1	Marg Brazelton	x6121	8	f	t	2020-10-04 20:45:01.47671	2020-10-04 22:40:14.835648
9	Marnie Frith	x2378	28	f	t	2020-10-04 20:54:29.482772	2020-10-04 22:45:14.835648
13	Jacalyn Crews	x3359	18	f	t	2020-10-04 20:59:49.485142	2020-10-04 22:50:14.835648
8	Moises Newsom	x2590	22	f	t	2020-10-04 21:00:53.482221	2020-10-04 22:55:14.835648
12	Sharolyn Erb	x3630	12	f	t	2020-10-04 21:03:27.484561	2020-10-04 23:00:14.835648
7	Obdulia Delorenzo	x4946	25	f	t	2020-10-04 21:04:26.481813	2020-10-04 23:05:14.835648
20	Ericka Billups	x9838	7	t	t	2020-10-04 21:35:45.488604	2020-10-04 23:10:14.835648
17	Piper Rolan-Adeyemi	x3597	21	t	t	2020-10-04 21:59:46.487093	2020-10-04 23:15:14.835648
14	Lavada Golay	x3615	12	t	t	2020-10-04 22:01:59.485549	2020-10-04 23:20:14.835648
16	Jeri Sherrard	x5681	8	t	t	2020-10-04 22:03:17.486539	2020-10-04 23:25:14.835648
19	Evonne Granda	x2744	11	t	t	2020-10-04 22:05:38.487999	2020-10-04 23:30:14.835648
18	Willodean Delafuente	x6311	28	t	t	2020-10-04 22:07:03.487508	2020-10-04 23:35:14.835648
15	Serina Lacomb	x4138	11	t	t	2020-10-04 22:08:30.48603	2020-10-04 23:40:14.835648
3	Youlanda Zajicek	x2798	31	f	t	2020-10-04 21:09:03.479283	2020-10-04 23:08:14.835648
\.


--
-- Name: service_id_seq; Type: SEQUENCE SET; Schema: public; Owner: signout
--

SELECT pg_catalog.setval('public.service_id_seq', 32, true);


--
-- Name: signout_id_seq; Type: SEQUENCE SET; Schema: public; Owner: signout
--

SELECT pg_catalog.setval('public.signout_id_seq', 20, true);


--
-- Name: service service_pkey; Type: CONSTRAINT; Schema: public; Owner: signout
--

ALTER TABLE ONLY public.service
    ADD CONSTRAINT service_pkey PRIMARY KEY (id);


--
-- Name: signout signout_pkey; Type: CONSTRAINT; Schema: public; Owner: signout
--

ALTER TABLE ONLY public.signout
    ADD CONSTRAINT signout_pkey PRIMARY KEY (id);


--
-- Name: signout signout_service_fkey; Type: FK CONSTRAINT; Schema: public; Owner: signout
--

ALTER TABLE ONLY public.signout
    ADD CONSTRAINT signout_service_fkey FOREIGN KEY (service) REFERENCES public.service(id);


--
-- PostgreSQL database dump complete
--

