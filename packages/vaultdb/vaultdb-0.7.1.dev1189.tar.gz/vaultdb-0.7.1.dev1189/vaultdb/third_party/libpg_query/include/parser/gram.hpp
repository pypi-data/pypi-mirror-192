/* A Bison parser, made by GNU Bison 3.5.1.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2020 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Undocumented macros, especially those whose name start with YY_,
   are private implementation details.  Do not rely on them.  */

#ifndef YY_BASE_YY_THIRD_PARTY_LIBPG_QUERY_GRAMMAR_GRAMMAR_OUT_HPP_INCLUDED
# define YY_BASE_YY_THIRD_PARTY_LIBPG_QUERY_GRAMMAR_GRAMMAR_OUT_HPP_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int base_yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    IDENT = 258,
    FCONST = 259,
    SCONST = 260,
    BCONST = 261,
    XCONST = 262,
    Op = 263,
    ICONST = 264,
    PARAM = 265,
    TYPECAST = 266,
    DOT_DOT = 267,
    COLON_EQUALS = 268,
    EQUALS_GREATER = 269,
    POWER_OF = 270,
    LAMBDA_ARROW = 271,
    DOUBLE_ARROW = 272,
    LESS_EQUALS = 273,
    GREATER_EQUALS = 274,
    NOT_EQUALS = 275,
    ABORT_P = 276,
    ABSOLUTE_P = 277,
    ACCESS = 278,
    ACTION = 279,
    ADD_P = 280,
    ADMIN = 281,
    AFTER = 282,
    AGGREGATE = 283,
    ALL = 284,
    ALSO = 285,
    ALTER = 286,
    ALWAYS = 287,
    ANALYSE = 288,
    ANALYZE = 289,
    AND = 290,
    ANY = 291,
    ARRAY = 292,
    AS = 293,
    ASC_P = 294,
    ASSERTION = 295,
    ASSIGNMENT = 296,
    ASYMMETRIC = 297,
    AT = 298,
    ATTACH = 299,
    ATTRIBUTE = 300,
    AUTHORIZATION = 301,
    BACKWARD = 302,
    BEFORE = 303,
    BEGIN_P = 304,
    BETWEEN = 305,
    BIGINT = 306,
    BINARY = 307,
    BIT = 308,
    BOOLEAN_P = 309,
    BOTH = 310,
    BY = 311,
    CACHE = 312,
    CALL_P = 313,
    CALLED = 314,
    CASCADE = 315,
    CASCADED = 316,
    CASE = 317,
    CAST = 318,
    CATALOG_P = 319,
    CHAIN = 320,
    CHAR_P = 321,
    CHARACTER = 322,
    CHARACTERISTICS = 323,
    CHECK_P = 324,
    CHECKPOINT = 325,
    CLASS = 326,
    CLOSE = 327,
    CLUSTER = 328,
    COALESCE = 329,
    COLLATE = 330,
    COLLATION = 331,
    COLUMN = 332,
    COLUMNS = 333,
    COMMENT = 334,
    COMMENTS = 335,
    COMMIT = 336,
    COMMITTED = 337,
    COMPRESSION = 338,
    CONCURRENTLY = 339,
    CONFIGURATION = 340,
    CONFLICT = 341,
    CONNECTION = 342,
    CONSTRAINT = 343,
    CONSTRAINTS = 344,
    CONTENT_P = 345,
    CONTINUE_P = 346,
    CONVERSION_P = 347,
    COPY = 348,
    COST = 349,
    CREATE_P = 350,
    CROSS = 351,
    CSV = 352,
    CUBE = 353,
    CURRENT_P = 354,
    CURRENT_CATALOG = 355,
    CURRENT_DATE = 356,
    CURRENT_ROLE = 357,
    CURRENT_SCHEMA = 358,
    CURRENT_TIME = 359,
    CURRENT_TIMESTAMP = 360,
    CURRENT_USER = 361,
    CURSOR = 362,
    CYCLE = 363,
    DATA_P = 364,
    DATABASE = 365,
    DAY_P = 366,
    DAYS_P = 367,
    DEALLOCATE = 368,
    DEC = 369,
    DECIMAL_P = 370,
    DECLARE = 371,
    DEFAULT = 372,
    DEFAULTS = 373,
    DEFERRABLE = 374,
    DEFERRED = 375,
    DEFINER = 376,
    DELETE_P = 377,
    DELIMITER = 378,
    DELIMITERS = 379,
    DEPENDS = 380,
    DESC_P = 381,
    DESCRIBE = 382,
    DETACH = 383,
    DICTIONARY = 384,
    DISABLE_P = 385,
    DISCARD = 386,
    DISTINCT = 387,
    DO = 388,
    DOCUMENT_P = 389,
    DOMAIN_P = 390,
    DOUBLE_P = 391,
    DROP = 392,
    EACH = 393,
    ELSE = 394,
    ENABLE_P = 395,
    ENCODING = 396,
    ENCRYPTED = 397,
    END_P = 398,
    ENUM_P = 399,
    ESCAPE = 400,
    EVENT = 401,
    EXCEPT = 402,
    EXCLUDE = 403,
    EXCLUDING = 404,
    EXCLUSIVE = 405,
    EXECUTE = 406,
    EXISTS = 407,
    EXPLAIN = 408,
    EXPORT_P = 409,
    EXPORT_STATE = 410,
    EXTENSION = 411,
    EXTERNAL = 412,
    EXTRACT = 413,
    FALSE_P = 414,
    FAMILY = 415,
    FETCH = 416,
    FILTER = 417,
    FIRST_P = 418,
    FLOAT_P = 419,
    FOLLOWING = 420,
    FOR = 421,
    FORCE = 422,
    FOREIGN = 423,
    FORTRESS = 424,
    FORWARD = 425,
    FREEZE = 426,
    FROM = 427,
    FULL = 428,
    FUNCTION = 429,
    FUNCTIONS = 430,
    GENERATED = 431,
    GLOB = 432,
    GLOBAL = 433,
    GRANT = 434,
    GRANTED = 435,
    GROUP_P = 436,
    GROUPING = 437,
    GROUPING_ID = 438,
    HANDLER = 439,
    HAVING = 440,
    HEADER_P = 441,
    HOLD = 442,
    HOUR_P = 443,
    HOURS_P = 444,
    IDENTITY_P = 445,
    IF_P = 446,
    IGNORE_P = 447,
    ILIKE = 448,
    IMMEDIATE = 449,
    IMMUTABLE = 450,
    IMPLICIT_P = 451,
    IMPORT_P = 452,
    IN_P = 453,
    INCLUDING = 454,
    INCREMENT = 455,
    INDEX = 456,
    INDEXES = 457,
    INHERIT = 458,
    INHERITS = 459,
    INITIALLY = 460,
    INLINE_P = 461,
    INNER_P = 462,
    INOUT = 463,
    INPUT_P = 464,
    INSENSITIVE = 465,
    INSERT = 466,
    INSTALL = 467,
    INSTEAD = 468,
    INT_P = 469,
    INTEGER = 470,
    INTERSECT = 471,
    INTERVAL = 472,
    INTO = 473,
    INVOKER = 474,
    IS = 475,
    ISNULL = 476,
    ISOLATION = 477,
    JOIN = 478,
    JSON = 479,
    KEY = 480,
    LABEL = 481,
    LANGUAGE = 482,
    LARGE_P = 483,
    LAST_P = 484,
    LATERAL_P = 485,
    LEADING = 486,
    LEAKPROOF = 487,
    LEFT = 488,
    LEVEL = 489,
    LIKE = 490,
    LIMIT = 491,
    LISTEN = 492,
    LOAD = 493,
    LOCAL = 494,
    LOCALTIME = 495,
    LOCALTIMESTAMP = 496,
    LOCATION = 497,
    LOCK_P = 498,
    LOCKED = 499,
    LOGGED = 500,
    LOGIN = 501,
    MACRO = 502,
    MAP = 503,
    MAPPING = 504,
    MATCH = 505,
    MATERIALIZED = 506,
    MAXVALUE = 507,
    METHOD = 508,
    MICROSECOND_P = 509,
    MICROSECONDS_P = 510,
    MILLISECOND_P = 511,
    MILLISECONDS_P = 512,
    MINUTE_P = 513,
    MINUTES_P = 514,
    MINVALUE = 515,
    MODE = 516,
    MONTH_P = 517,
    MONTHS_P = 518,
    MOVE = 519,
    NAME_P = 520,
    NAMES = 521,
    NATIONAL = 522,
    NATURAL = 523,
    NCHAR = 524,
    NEW = 525,
    NEXT = 526,
    NO = 527,
    NOLOGIN = 528,
    NONE = 529,
    NOSUPERUSER = 530,
    NOT = 531,
    NOTHING = 532,
    NOTIFY = 533,
    NOTNULL = 534,
    NOWAIT = 535,
    NULL_P = 536,
    NULLIF = 537,
    NULLS_P = 538,
    NUMERIC = 539,
    OBJECT_P = 540,
    OF = 541,
    OFF = 542,
    OFFSET = 543,
    OIDS = 544,
    OLD = 545,
    ON = 546,
    ONLY = 547,
    OPERATOR = 548,
    OPTION = 549,
    OPTIONS = 550,
    OR = 551,
    ORDER = 552,
    ORDINALITY = 553,
    OUT_P = 554,
    OUTER_P = 555,
    OVER = 556,
    OVERLAPS = 557,
    OVERLAY = 558,
    OVERRIDING = 559,
    OWNED = 560,
    OWNER = 561,
    PARALLEL = 562,
    PARSER = 563,
    PARTIAL = 564,
    PARTITION = 565,
    PASSING = 566,
    PASSWORD = 567,
    PERCENT = 568,
    PLACING = 569,
    PLANS = 570,
    POLICY = 571,
    POSITION = 572,
    POSITIONAL = 573,
    PRAGMA_P = 574,
    PRECEDING = 575,
    PRECISION = 576,
    PREPARE = 577,
    PREPARED = 578,
    PRESERVE = 579,
    PRIMARY = 580,
    PRIOR = 581,
    PRIVILEGES = 582,
    PROCEDURAL = 583,
    PROCEDURE = 584,
    PROGRAM = 585,
    PUBLICATION = 586,
    QUALIFY = 587,
    QUOTE = 588,
    RANGE = 589,
    READ_P = 590,
    REAL = 591,
    REASSIGN = 592,
    RECHECK = 593,
    RECURSIVE = 594,
    REF = 595,
    REFERENCES = 596,
    REFERENCING = 597,
    REFRESH = 598,
    REINDEX = 599,
    RELATIVE_P = 600,
    RELEASE = 601,
    RENAME = 602,
    REPEATABLE = 603,
    REPLACE = 604,
    REPLICA = 605,
    RESET = 606,
    RESPECT_P = 607,
    RESTART = 608,
    RESTRICT = 609,
    RETURNING = 610,
    RETURNS = 611,
    REVOKE = 612,
    RIGHT = 613,
    ROLE = 614,
    ROLLBACK = 615,
    ROLLUP = 616,
    ROW = 617,
    ROWS = 618,
    RULE = 619,
    SAMPLE = 620,
    SAVEPOINT = 621,
    SCHEMA = 622,
    SCHEMAS = 623,
    SCROLL = 624,
    SEARCH = 625,
    SECOND_P = 626,
    SECONDS_P = 627,
    SECURITY = 628,
    SELECT = 629,
    SEQUENCE = 630,
    SEQUENCES = 631,
    SERIALIZABLE = 632,
    SERVER = 633,
    SESSION = 634,
    SESSION_USER = 635,
    SET = 636,
    SETOF = 637,
    SETS = 638,
    SHARE = 639,
    SHOW = 640,
    SIMILAR = 641,
    SIMPLE = 642,
    SKIP = 643,
    SMALLINT = 644,
    SNAPSHOT = 645,
    SOME = 646,
    SQL_P = 647,
    STABLE = 648,
    STANDALONE_P = 649,
    START = 650,
    STATEMENT = 651,
    STATISTICS = 652,
    STDIN = 653,
    STDOUT = 654,
    STORAGE = 655,
    STORED = 656,
    STRICT_P = 657,
    STRIP_P = 658,
    STRUCT = 659,
    SUBSCRIPTION = 660,
    SUBSTRING = 661,
    SUMMARIZE = 662,
    SUPERUSER = 663,
    SYMMETRIC = 664,
    SYSID = 665,
    SYSTEM_P = 666,
    TABLE = 667,
    TABLES = 668,
    TABLESAMPLE = 669,
    TABLESPACE = 670,
    TAG = 671,
    TEMP = 672,
    TEMPLATE = 673,
    TEMPORARY = 674,
    TEXT_P = 675,
    THEN = 676,
    TIME = 677,
    TIMESTAMP = 678,
    TO = 679,
    TRAILING = 680,
    TRANSACTION = 681,
    TRANSFORM = 682,
    TREAT = 683,
    TRIGGER = 684,
    TRIM = 685,
    TRUE_P = 686,
    TRUNCATE = 687,
    TRUSTED = 688,
    TRY_CAST = 689,
    TYPE_P = 690,
    TYPES_P = 691,
    UNBOUNDED = 692,
    UNCOMMITTED = 693,
    UNENCRYPTED = 694,
    UNION = 695,
    UNIQUE = 696,
    UNKNOWN = 697,
    UNLISTEN = 698,
    UNLOCK = 699,
    UNLOGGED = 700,
    UNTIL = 701,
    UPDATE = 702,
    USE_P = 703,
    USER = 704,
    USING = 705,
    VACUUM = 706,
    VALID = 707,
    VALIDATE = 708,
    VALIDATOR = 709,
    VALUE_P = 710,
    VALUES = 711,
    VARCHAR = 712,
    VARIADIC = 713,
    VARYING = 714,
    VERBOSE = 715,
    VERSION_P = 716,
    VIEW = 717,
    VIEWS = 718,
    VIRTUAL = 719,
    VOLATILE = 720,
    WHEN = 721,
    WHERE = 722,
    WHITESPACE_P = 723,
    WINDOW = 724,
    WITH = 725,
    WITHIN = 726,
    WITHOUT = 727,
    WORK = 728,
    WRAPPER = 729,
    WRITE_P = 730,
    XML_P = 731,
    XMLATTRIBUTES = 732,
    XMLCONCAT = 733,
    XMLELEMENT = 734,
    XMLEXISTS = 735,
    XMLFOREST = 736,
    XMLNAMESPACES = 737,
    XMLPARSE = 738,
    XMLPI = 739,
    XMLROOT = 740,
    XMLSERIALIZE = 741,
    XMLTABLE = 742,
    YEAR_P = 743,
    YEARS_P = 744,
    YES_P = 745,
    ZONE = 746,
    NOT_LA = 747,
    NULLS_LA = 748,
    WITH_LA = 749,
    POSTFIXOP = 750,
    UMINUS = 751
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 14 "third_party/libpg_query/grammar/grammar.y"

	core_YYSTYPE		core_yystype;
	/* these fields must match core_YYSTYPE: */
	int					ival;
	char				*str;
	const char			*keyword;
	const char          *conststr;

	char				chr;
	bool				boolean;
	PGJoinType			jtype;
	PGDropBehavior		dbehavior;
	PGOnCommitAction		oncommit;
	PGOnCreateConflict		oncreateconflict;
	PGList				*list;
	PGNode				*node;
	PGValue				*value;
	PGObjectType			objtype;
	PGTypeName			*typnam;
	PGObjectWithArgs		*objwithargs;
	PGDefElem				*defelt;
	PGSortBy				*sortby;
	PGWindowDef			*windef;
	PGJoinExpr			*jexpr;
	PGIndexElem			*ielem;
	PGAlias				*alias;
	PGRangeVar			*range;
	PGIntoClause			*into;
	PGWithClause			*with;
	PGInferClause			*infer;
	PGOnConflictClause	*onconflict;
	PGOnConflictActionAlias onconflictshorthand;
	PGAIndices			*aind;
	PGResTarget			*target;
	PGInsertStmt			*istmt;
	PGVariableSetStmt		*vsetstmt;
	PGOverridingKind       override;
	PGSortByDir            sortorder;
	PGSortByNulls          nullorder;
	PGConstrType           constr;
	PGLockClauseStrength lockstrength;
	PGLockWaitPolicy lockwaitpolicy;
	PGSubLinkType subquerytype;
	PGViewCheckOption viewcheckoption;

#line 600 "third_party/libpg_query/grammar/grammar_out.hpp"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif



int base_yyparse (core_yyscan_t yyscanner);

#endif /* !YY_BASE_YY_THIRD_PARTY_LIBPG_QUERY_GRAMMAR_GRAMMAR_OUT_HPP_INCLUDED  */
