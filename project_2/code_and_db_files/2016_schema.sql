--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)

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

ALTER TABLE IF EXISTS ONLY public."2016_book_order" DROP CONSTRAINT IF EXISTS book_order_2016_order_order_id_fk;
ALTER TABLE IF EXISTS ONLY public."2016_book_order" DROP CONSTRAINT IF EXISTS book_order_2016_book_book_id_fk;
ALTER TABLE IF EXISTS ONLY public."2016_user_address" DROP CONSTRAINT IF EXISTS "2016_user_has_address_2016_user_user_id_fk";
ALTER TABLE IF EXISTS ONLY public."2016_user_address" DROP CONSTRAINT IF EXISTS "2016_user_has_address_2016_address_address_id_fk";
ALTER TABLE IF EXISTS ONLY public."2016_publisher" DROP CONSTRAINT IF EXISTS "2016_publisher_2016_address_address_id_fk";
ALTER TABLE IF EXISTS ONLY public."2016_order" DROP CONSTRAINT IF EXISTS "2016_order_2016_user_user_id_fk";
ALTER TABLE IF EXISTS ONLY public."2016_order" DROP CONSTRAINT IF EXISTS "2016_order_2016_user_address_address_id_user_id_fk_2";
ALTER TABLE IF EXISTS ONLY public."2016_order" DROP CONSTRAINT IF EXISTS "2016_order_2016_user_address_address_id_user_id_fk";
ALTER TABLE IF EXISTS ONLY public."2016_book_review" DROP CONSTRAINT IF EXISTS "2016_book_has_review_2016_review_review_id_fk";
ALTER TABLE IF EXISTS ONLY public."2016_book_review" DROP CONSTRAINT IF EXISTS "2016_book_has_review_2016_book_book_id_fk";
ALTER TABLE IF EXISTS ONLY public."2016_book_author" DROP CONSTRAINT IF EXISTS "2016_book_has_authors_2016_book_book_id_fk";
ALTER TABLE IF EXISTS ONLY public."2016_book_author" DROP CONSTRAINT IF EXISTS "2016_book_has_authors_2016_author_author_id_fk";
ALTER TABLE IF EXISTS ONLY public."2016_book" DROP CONSTRAINT IF EXISTS "2016_book_2016_publisher_publisher_id_fk";
DROP INDEX IF EXISTS public."2016_user_username_uindex";
DROP INDEX IF EXISTS public."2016_user_email_uindex";
DROP INDEX IF EXISTS public."2016_order_order_id_uindex";
DROP INDEX IF EXISTS public."2016_book_isbn_uindex";
ALTER TABLE IF EXISTS ONLY public."2016_book_order" DROP CONSTRAINT IF EXISTS book_order_pk;
ALTER TABLE IF EXISTS ONLY public."2016_user" DROP CONSTRAINT IF EXISTS "2016_user_pk";
ALTER TABLE IF EXISTS ONLY public."2016_user_address" DROP CONSTRAINT IF EXISTS "2016_user_has_address_pk";
ALTER TABLE IF EXISTS ONLY public."2016_review" DROP CONSTRAINT IF EXISTS "2016_review_pk";
ALTER TABLE IF EXISTS ONLY public."2016_publisher" DROP CONSTRAINT IF EXISTS "2016_publisher_pk";
ALTER TABLE IF EXISTS ONLY public."2016_order" DROP CONSTRAINT IF EXISTS "2016_order_pk";
ALTER TABLE IF EXISTS ONLY public."2016_book" DROP CONSTRAINT IF EXISTS "2016_book_pk";
ALTER TABLE IF EXISTS ONLY public."2016_book_review" DROP CONSTRAINT IF EXISTS "2016_book_has_review_pk";
ALTER TABLE IF EXISTS ONLY public."2016_book_author" DROP CONSTRAINT IF EXISTS "2016_book_has_authors_pk";
ALTER TABLE IF EXISTS ONLY public."2016_author" DROP CONSTRAINT IF EXISTS "2016_author_pk";
ALTER TABLE IF EXISTS ONLY public."2016_address" DROP CONSTRAINT IF EXISTS "2016_address_pk";
ALTER TABLE IF EXISTS public."2016_user" ALTER COLUMN user_id DROP DEFAULT;
ALTER TABLE IF EXISTS public."2016_review" ALTER COLUMN review_id DROP DEFAULT;
ALTER TABLE IF EXISTS public."2016_publisher" ALTER COLUMN publisher_id DROP DEFAULT;
ALTER TABLE IF EXISTS public."2016_order" ALTER COLUMN order_id DROP DEFAULT;
ALTER TABLE IF EXISTS public."2016_book" ALTER COLUMN book_id DROP DEFAULT;
ALTER TABLE IF EXISTS public."2016_author" ALTER COLUMN author_id DROP DEFAULT;
ALTER TABLE IF EXISTS public."2016_address" ALTER COLUMN address_id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public."2016_user_user_id_seq";
DROP TABLE IF EXISTS public."2016_user_address";
DROP TABLE IF EXISTS public."2016_user";
DROP SEQUENCE IF EXISTS public."2016_review_review_id_seq";
DROP TABLE IF EXISTS public."2016_review";
DROP SEQUENCE IF EXISTS public."2016_publisher_publisher_id_seq";
DROP TABLE IF EXISTS public."2016_publisher";
DROP SEQUENCE IF EXISTS public."2016_order_order_id_seq";
DROP TABLE IF EXISTS public."2016_order";
DROP TABLE IF EXISTS public."2016_book_review";
DROP TABLE IF EXISTS public."2016_book_order";
DROP SEQUENCE IF EXISTS public."2016_book_book_id_seq";
DROP TABLE IF EXISTS public."2016_book_author";
DROP TABLE IF EXISTS public."2016_book";
DROP SEQUENCE IF EXISTS public."2016_author_author_id_seq";
DROP TABLE IF EXISTS public."2016_author";
DROP SEQUENCE IF EXISTS public."2016_address_address_id_seq";
DROP TABLE IF EXISTS public."2016_address";
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: 2016_address; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_address" (
    address_id bigint NOT NULL,
    address_name character varying NOT NULL,
    address_number integer NOT NULL,
    city character varying NOT NULL,
    country character varying NOT NULL,
    postal_code character varying NOT NULL
);


--
-- Name: 2016_address_address_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."2016_address_address_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: 2016_address_address_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."2016_address_address_id_seq" OWNED BY public."2016_address".address_id;


--
-- Name: 2016_author; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_author" (
    author_id bigint NOT NULL,
    gender character varying(6),
    name character varying NOT NULL,
    nationality character varying
);


--
-- Name: 2016_author_author_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."2016_author_author_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: 2016_author_author_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."2016_author_author_id_seq" OWNED BY public."2016_author".author_id;


--
-- Name: 2016_book; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_book" (
    book_id bigint NOT NULL,
    isbn character(10) NOT NULL,
    current_price numeric(6,2),
    description text,
    publication_year character(4),
    title character varying(200),
    publisher_id bigint
);


--
-- Name: 2016_book_author; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_book_author" (
    author_id bigint NOT NULL,
    book_id bigint NOT NULL,
    author_ordinal smallint DEFAULT 0 NOT NULL,
    role character varying
);


--
-- Name: 2016_book_book_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."2016_book_book_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: 2016_book_book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."2016_book_book_id_seq" OWNED BY public."2016_book".book_id;


--
-- Name: 2016_book_order; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_book_order" (
    book_id bigint NOT NULL,
    order_id bigint NOT NULL,
    quantity integer DEFAULT 1 NOT NULL
);


--
-- Name: 2016_book_review; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_book_review" (
    book_id bigint NOT NULL,
    review_id bigint NOT NULL
);


--
-- Name: 2016_order; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_order" (
    order_id bigint NOT NULL,
    user_id bigint NOT NULL,
    billing_address_id bigint NOT NULL,
    shipping_address_id bigint NOT NULL,
    placement timestamp with time zone NOT NULL,
    completed timestamp with time zone
);


--
-- Name: 2016_order_order_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."2016_order_order_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: 2016_order_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."2016_order_order_id_seq" OWNED BY public."2016_order".order_id;


--
-- Name: 2016_publisher; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_publisher" (
    publisher_id bigint NOT NULL,
    name character varying NOT NULL,
    phone_number character varying,
    address_id bigint
);


--
-- Name: 2016_publisher_publisher_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."2016_publisher_publisher_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: 2016_publisher_publisher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."2016_publisher_publisher_id_seq" OWNED BY public."2016_publisher".publisher_id;


--
-- Name: 2016_review; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_review" (
    review_id bigint NOT NULL,
    created timestamp with time zone,
    nickname character varying DEFAULT 'anonymous'::character varying NOT NULL,
    score smallint NOT NULL,
    text text NOT NULL
);


--
-- Name: 2016_review_review_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."2016_review_review_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: 2016_review_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."2016_review_review_id_seq" OWNED BY public."2016_review".review_id;


--
-- Name: 2016_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_user" (
    user_id bigint NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    phone_number character varying NOT NULL,
    real_name character varying NOT NULL
);


--
-- Name: 2016_user_address; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."2016_user_address" (
    address_id bigint NOT NULL,
    user_id bigint NOT NULL,
    is_physical boolean DEFAULT true NOT NULL,
    is_shipping boolean DEFAULT true NOT NULL,
    is_billing boolean DEFAULT true NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


--
-- Name: 2016_user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."2016_user_user_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: 2016_user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."2016_user_user_id_seq" OWNED BY public."2016_user".user_id;


--
-- Name: 2016_address address_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_address" ALTER COLUMN address_id SET DEFAULT nextval('public."2016_address_address_id_seq"'::regclass);


--
-- Name: 2016_author author_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_author" ALTER COLUMN author_id SET DEFAULT nextval('public."2016_author_author_id_seq"'::regclass);


--
-- Name: 2016_book book_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book" ALTER COLUMN book_id SET DEFAULT nextval('public."2016_book_book_id_seq"'::regclass);


--
-- Name: 2016_order order_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_order" ALTER COLUMN order_id SET DEFAULT nextval('public."2016_order_order_id_seq"'::regclass);


--
-- Name: 2016_publisher publisher_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_publisher" ALTER COLUMN publisher_id SET DEFAULT nextval('public."2016_publisher_publisher_id_seq"'::regclass);


--
-- Name: 2016_review review_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_review" ALTER COLUMN review_id SET DEFAULT nextval('public."2016_review_review_id_seq"'::regclass);


--
-- Name: 2016_user user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_user" ALTER COLUMN user_id SET DEFAULT nextval('public."2016_user_user_id_seq"'::regclass);


--
-- Name: 2016_address 2016_address_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_address"
    ADD CONSTRAINT "2016_address_pk" PRIMARY KEY (address_id);


--
-- Name: 2016_author 2016_author_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_author"
    ADD CONSTRAINT "2016_author_pk" PRIMARY KEY (author_id);


--
-- Name: 2016_book_author 2016_book_has_authors_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book_author"
    ADD CONSTRAINT "2016_book_has_authors_pk" PRIMARY KEY (author_id, book_id);


--
-- Name: 2016_book_review 2016_book_has_review_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book_review"
    ADD CONSTRAINT "2016_book_has_review_pk" PRIMARY KEY (book_id, review_id);


--
-- Name: 2016_book 2016_book_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book"
    ADD CONSTRAINT "2016_book_pk" PRIMARY KEY (book_id);


--
-- Name: 2016_order 2016_order_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_order"
    ADD CONSTRAINT "2016_order_pk" PRIMARY KEY (user_id, order_id);


--
-- Name: 2016_publisher 2016_publisher_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_publisher"
    ADD CONSTRAINT "2016_publisher_pk" PRIMARY KEY (publisher_id);


--
-- Name: 2016_review 2016_review_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_review"
    ADD CONSTRAINT "2016_review_pk" PRIMARY KEY (review_id);


--
-- Name: 2016_user_address 2016_user_has_address_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_user_address"
    ADD CONSTRAINT "2016_user_has_address_pk" PRIMARY KEY (address_id, user_id);


--
-- Name: 2016_user 2016_user_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_user"
    ADD CONSTRAINT "2016_user_pk" PRIMARY KEY (user_id);


--
-- Name: 2016_book_order book_order_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book_order"
    ADD CONSTRAINT book_order_pk PRIMARY KEY (book_id, order_id);


--
-- Name: 2016_book_isbn_uindex; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "2016_book_isbn_uindex" ON public."2016_book" USING btree (isbn);


--
-- Name: 2016_order_order_id_uindex; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "2016_order_order_id_uindex" ON public."2016_order" USING btree (order_id);


--
-- Name: 2016_user_email_uindex; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "2016_user_email_uindex" ON public."2016_user" USING btree (email);


--
-- Name: 2016_user_username_uindex; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "2016_user_username_uindex" ON public."2016_user" USING btree (username);


--
-- Name: 2016_book 2016_book_2016_publisher_publisher_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book"
    ADD CONSTRAINT "2016_book_2016_publisher_publisher_id_fk" FOREIGN KEY (publisher_id) REFERENCES public."2016_publisher"(publisher_id) ON DELETE SET NULL;


--
-- Name: 2016_book_author 2016_book_has_authors_2016_author_author_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book_author"
    ADD CONSTRAINT "2016_book_has_authors_2016_author_author_id_fk" FOREIGN KEY (author_id) REFERENCES public."2016_author"(author_id);


--
-- Name: 2016_book_author 2016_book_has_authors_2016_book_book_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book_author"
    ADD CONSTRAINT "2016_book_has_authors_2016_book_book_id_fk" FOREIGN KEY (book_id) REFERENCES public."2016_book"(book_id);


--
-- Name: 2016_book_review 2016_book_has_review_2016_book_book_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book_review"
    ADD CONSTRAINT "2016_book_has_review_2016_book_book_id_fk" FOREIGN KEY (book_id) REFERENCES public."2016_book"(book_id);


--
-- Name: 2016_book_review 2016_book_has_review_2016_review_review_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book_review"
    ADD CONSTRAINT "2016_book_has_review_2016_review_review_id_fk" FOREIGN KEY (review_id) REFERENCES public."2016_review"(review_id);


--
-- Name: 2016_order 2016_order_2016_user_address_address_id_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_order"
    ADD CONSTRAINT "2016_order_2016_user_address_address_id_user_id_fk" FOREIGN KEY (billing_address_id, user_id) REFERENCES public."2016_user_address"(address_id, user_id);


--
-- Name: 2016_order 2016_order_2016_user_address_address_id_user_id_fk_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_order"
    ADD CONSTRAINT "2016_order_2016_user_address_address_id_user_id_fk_2" FOREIGN KEY (shipping_address_id, user_id) REFERENCES public."2016_user_address"(address_id, user_id);


--
-- Name: 2016_order 2016_order_2016_user_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_order"
    ADD CONSTRAINT "2016_order_2016_user_user_id_fk" FOREIGN KEY (user_id) REFERENCES public."2016_user"(user_id);


--
-- Name: 2016_publisher 2016_publisher_2016_address_address_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_publisher"
    ADD CONSTRAINT "2016_publisher_2016_address_address_id_fk" FOREIGN KEY (address_id) REFERENCES public."2016_address"(address_id) ON DELETE SET NULL;


--
-- Name: 2016_user_address 2016_user_has_address_2016_address_address_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_user_address"
    ADD CONSTRAINT "2016_user_has_address_2016_address_address_id_fk" FOREIGN KEY (address_id) REFERENCES public."2016_address"(address_id);


--
-- Name: 2016_user_address 2016_user_has_address_2016_user_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_user_address"
    ADD CONSTRAINT "2016_user_has_address_2016_user_user_id_fk" FOREIGN KEY (user_id) REFERENCES public."2016_user"(user_id);


--
-- Name: 2016_book_order book_order_2016_book_book_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book_order"
    ADD CONSTRAINT book_order_2016_book_book_id_fk FOREIGN KEY (book_id) REFERENCES public."2016_book"(book_id);


--
-- Name: 2016_book_order book_order_2016_order_order_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."2016_book_order"
    ADD CONSTRAINT book_order_2016_order_order_id_fk FOREIGN KEY (order_id) REFERENCES public."2016_order"(order_id);


--
-- PostgreSQL database dump complete
--

