# A demo Python REST API project showing how to write a small microservice while avoiding some common mistakes

Writing a microservice using one of micro-frameworks might seem like an easy task if you are an intermediate programmer, in which case you are wrong. It takes a lot of ingredients to cook up a production ready service.

It might seem outright impossible if you are a beginner, in which casae you are also wrong. It is significantly easier to write a service in Python these days, thanks to amazing libraries that are such a huge part of what makes Python great.

This repo aims to demonstrate some, just some, of the many ways this can be done, in a beginner friendly way that is easy to follow and recreate.


## Table of contents
- [A demo Python REST API project showing how to write a small microservice while avoiding some common mistakes](#a-demo-python-rest-api-project-showing-how-to-write-a-small-microservice-while-avoiding-some-common-mistakes)
  - [Table of contents](#table-of-contents)
  - [Caveat emptor](#caveat-emptor)
  - [Handling and serving the API](#handling-and-serving-the-api)
  - [Data processing](#data-processing)
  - [Database](#database)
  - [Good REST API design](#good-rest-api-design)
  - [Not blocking the main thread](#not-blocking-the-main-thread)
  - [Structured Logging](#structured-logging)
  - [Metrics](#metrics)
  - [Documentation](#documentation)
  - [Unit tests](#unit-tests)
  - [API tests](#api-tests)
  - [Mocking](#mocking)
  - [Coverage](#coverage)
  - [Shipt it!](#shipt-it)
    - [Manage it](#manage-it)
    - [Update it](#update-it)
    - [Secure it](#secure-it)
    - [Package it](#package-it)
    - [Host and deploy it](#host-and-deploy-it)
      - [VPS](#vps)
      - [Deploy to AWS Lambda](#deploy-to-aws-lambda)
      - [Deploy it somewhere else](#deploy-it-somewhere-else)
    - [Put a badge on it](#put-a-badge-on-it)
  - [That is all folks](#that-is-all-folks)
  - [Opportunities for improvement](#opportunities-for-improvement)
  - [How to run stuff](#how-to-run-stuff)


## Caveat emptor

Of course you should do your own research, and actually read the docs before deploying any of this to production and / or using it for serving actual users. Our industry moves at a rapid pace, and even if some of this was correct and accurate at some point in the past does not mean it is right now.

This is tailored as a demonstration for beginners, maybe one day it will evolve into a proper, production-ready example, but right now focus is _educational_.

_You_ are responsible for what _you believe_ and what _you deploy_!



## Handling and serving the API

[FastAPI](https://fastapi.tiangolo.com/)

FastAPI is amazing. It does so much that it is hard to summarize, I highly recommend checking the docs!

A common beginner mistake is to use something like [Flask](https://flask.palletsprojects.com) or [Bottle](https://bottlepy.org).

Flask is really for very experienced programmers who _already know what they are doing_. It is very easy to make serious mistakes with Flask, simply by omission. FastAPI is a much better option, as it already handles many gotchas for you and implements a ton of best practices.

That said, sometimes one does want to reinvent the wheel, and / or do something that is more precisely suited for their use case, in such situations you might eventually find yourself implementing your own REST API framework, how does one do that? well for one way of doing it check out Bottle for inspiration, it is a single Python file and is a full, albeit simple, framework.



## Data processing

[JSON](https://docs.python.org/3/library/json.html)

[CSV](https://docs.python.org/3/library/csv.html)

Python is batteries-included, the Python Standard Library comes with a ton of useful modules, JSON and CSV ones among them.

[JSON](https://www.json.org/json-en.html) is the language of the web, for better or worse, so it is important to support it in a microservice no matter what other formats one implements.

Here we use [Pydantic](https://pydantic-docs.helpmanual.io) a lot.

That said, it is important to understand that there are higher performance libraries availalbe for serious production data crunching such as [orjson](https://github.com/ijl/orjson), _if processing huge amounts of JSON and it is a bottleneck_. Pydantic uses [ultrajson](https://github.com/ultrajson/ultrajson).



## Database

[SQLite](https://www.sqlite.org)

[Python SQLite](https://docs.python.org/3/library/sqlite3.html)

Once you process data you want to store it somewhere, and SQLite is a great option.

It is the world's most, and arguably [best tested database](https://www.sqlite.org/testing.html), it tries to be like [PostgreSQL](http://www.postgresql.org) in the SQL it supports, and it can be deployed in cloud / production friendly ways, f.e. look at [Litestream](https://litestream.io) which is used by [Tailscale guys](https://tailscale.com/blog/database-for-2022/).

Of course a database is not necessary, and SQLite is not the only database, but this is one of the best default setups there is, and it works great for production. For some other production friendly options you could consider storing data directly in cloud object storage too, or millions of other ways of doing it, depending on what specifically is your use case.



## Good REST API design

[REST API Best Practices – REST Endpoint Design Examples](https://www.freecodecamp.org/news/rest-api-best-practices-rest-endpoint-design-examples/)

Correct API design is important, and it is not hard, especially for simpler APIs. But almost every successful complex API was also once a simpler one. It is important to also follow practices that will support the evolution of the API, including understanding that breaking changes do happen, and unlesss we design with that knowledge it will result in a terrible user experience.



## Not blocking the main thread

Threading in Python is still mostly to be avoided, the battle tested [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) module is preferential almost in every situation, except IO bound work. The GIL is still very much there, and the [latest efforts from Microsoft](https://github.com/colesbury/nogil) to remove it have not yet made it to the mainline.

There is a relatively newer kid on the Python block, in the form of [asyncio](https://docs.python.org/3/library/asyncio.html). Writing asynchronous code is not easy, multiprocessing is usually easier for beginners.

FastAPI has good [support for async](https://fastapi.tiangolo.com/async/), so in cases when it is needed, you should definitely consider using it.

There also is [Twisted](https://www.twistedmatrix.com/trac/) of course. But I have personally never used it, so cannot talk much about it.

Personally, I still find the Python / TypeScript `async / await` style of writing async code ugly and cumbersome and much prefer the approaches in Go ([fancier CSP](https://stackoverflow.com/a/32696464/4669203) but avoid channels for the most part, although channels are nicer now after the [addition of Generics](https://go.dev/doc/tutorial/generics) to Go), Zig ([async / await but done better](https://kristoff.it/blog/zig-colorblind-async-await/)) and especially [Erlang/OTP](https://www.erlang.org) or [Elixir](https://elixir-lang.org). In general writing correct concurrent code is very difficult, and many studies have shown that one or another approach changes this very little, in my mind it remains one of the things that are strongly affected by one's style, but it is never as simple as that because one does not produce great software alone, most of the time. To quote Robert L. Read:

> To be a good programmer is difficult and noble. The hardest part of making real a collective vision of a software project is dealing with one's coworkers and customers. Writing computer programs is important and takes great intelligence and skill. But it is really child's play compared to everything else that a good programmer must do to make a software system that succeeds for both the customer and myriad colleagues for whom she is partially responsible.



## Structured Logging

[Structlog](https://www.structlog.org)

[Structured logging in Python](https://newrelic.com/blog/how-to-relic/python-structured-logging)

Writing useful logs is important, especially in the age of the cloud and microservices, however the usual text logging facilities are a bad fit for this. It is important to write logs in an easy to parse, easy to query way, with good contextual information along the critical path in the program.

Structlog library lets one do this easily in Python. As usual, there are other options too.



## Metrics

[OpenTelementry](http://opentelemetry.io)

[Logs and metrics are not the same thing!](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/ch04.html). Both serve a purpose, and both are necessary when writing cloud native software.

Both serve the same purpose, to ease troubleshooting, understand performance, and of course to create KPIs that let us measure customer experience and product health.

Both have [pros and cons](https://grafana.com/blog/2016/01/05/logs-and-metrics-and-graphs-oh-my/).

In this project we use OpenTelemetry, the emerging choice to implement metrics in your language of choice.

Few other things to consider would be distributed tracing, eBPF, profiling, and so on, but we do not delve into that here, yet. Although do consider looking into supporting distributed tracing, as it is [supported using OpenTelemetry]((https://opentelemetry-python.readthedocs.io/en/stable/api/trace.html)), the same toolkit we used for adding metrics. In the context of a single service distributed service obviously has limited usefulness, but in the real world a company rarely runs a single service.



## Documentation

Documentation is not optional. Writing undocumented code is one of the worst pratices a programmer can get used to, so it is important to learn to write early on, and to stick to it!

It is especially important to write about _why the things are done the way they are_, not how they are done. It is very rare in _idiomatic_ Python that the code is so complex that one could justify explaining what it is doing in a comment, but if it is, well then of course you better do it!

API documentation in this project gets autogenerated, thanks to FastAPI, but as you see I also include a lot of infromation in this README and in the code as comments. Some people would say too much, but in the world where remote work is more and more becoming an option it is important to remember that [overcommunicating is less damaging than undercommunicating](https://pumble.com/blog/overcommunication/) and that reference material is exteremely handy when people on the other side of the globe are asleep.

It is also exteremely easy to test documentation both [in Python](https://docs.python.org/3/library/doctest.html) and [in Go](https://pkg.go.dev/testing#hdr-Examples). So the questions of whether to write or not to write good documentation with examples fast becomes a definitive: why not!?



## Unit tests

Modern python testing means using [Pytest](), the excellent framework that makes writing tests a joy. If you don't already know about Pytest, you stop doing whatever else you are doing and learn more about it!

Pytest integrates nicely wit VC Code, PyCharm and many other IDEs, has an extensive plugin ecosystem and can be used effectively from CLI too.

Writing test is important, fun, and noble, but it is not the end of the story. For example consider looking into [Atheris](https://github.com/google/atheris/) and [Hypothesis](https://hypothesis.readthedocs.io). Once again Go actually has Python beat here, as there is excellent automatic fuzzing [support in the standard toolchain](https://go.dev/doc/tutorial/fuzz).



## API tests

It is important to not only test the logic and the data processing code, but to also test the service as a whole. That is where API tests come in. Thankfully [FastAPI comes with excellent support for them](https://fastapi.tiangolo.com/tutorial/testing/). Writing API tests shouldn not be a hassle.

The `tests/api-tests` directory also contains few other ways of testing the API, f.e. using [HTTPie](https://httpie.io) in `api.sh` and using [VS Code REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) in `api.http`, the latter is also mostly usable in JetBrains products and they have a built in [HTTP Client](https://www.jetbrains.com/help/idea/http-client-in-product-code-editor.html).

If you want to do exploratory API testing, [Insomnia](https://insomnia.rest) is also a great open source way of doing it, instead of using the commercial Postman.



## Mocking

It is important to test the right thing. We want to test our stuff, not third party stuff, that should have it's own tests. Sometimes more control over the values of attributes, objects and environment variables is required, and in some cases it is required to present sepcific filesystem views. All of this is supported using following tools, to name a few:

- https://jmcgeheeiv.github.io/pyfakefs/release/usage.html
- https://docs.python.org/3/library/unittest.mock.html
- https://docs.pytest.org/en/6.2.x/monkeypatch.html
- https://docs.pytest.org/en/6.2.x/tmpdir.html

When working with SQLite it is also possible to specify `:memory:` as the database to keep the databse in memory, quite handy for testing.

API tests require mocking the http requests / responses, but it is actually more practical to just serve the requests over a mock instance. Some tools at our disposal for this are:

- https://fastapi.tiangolo.com/tutorial/testing/
- https://github.com/csernazs/pytest-httpserver

Of course this all works great with Pytest, which is waht you should always use.



## Coverage

There are two types of coverage that we need to be aware of, coverage of application functionality and coverage of code.

Coverage can be a very helpful, easy to grasp measure of software quality. For this reason it is often used in all sorts of companies from startups to large enterprises.

70% and higher coverage is usually a sign that software is well maintained, and is reliable. However, it is easy to [misuse](http://www.exampler.com/testing-com/writings/coverage.pdf) coverage metrics.

> If you make a certain level of coverage a target, people will try to attain it. The trouble is that high coverage numbers are too easy to reach with low quality testing.
>
>   -- Martin Fowler, [TestCoverage](https://martinfowler.com/bliki/TestCoverage.html)

Like any other kind of test, coverage is just a tool in the quest of improving sotware quality, it is not a goal in itself.

In this project we measure coverage using [Pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) plugin, along with Poetry.



## Shipt it!

Once we have everything working, it is important to also have at least some basic understanding of how the actual project would be shipped for production. How do we generate the final artifact? How do we deploy it? These are questions that can be much harder than actually implementing a simple service.

This is made worse by the fact that the beginner usually does not know that there are simple options available for this too.

Let's have a look at a setup tailored to be very simple and also cheap.



### Manage it

A very important aspect of any serious project is establishing a high quality, cohesive style for the project that help ensure everyone is on the same page. In Go code styling is a solved problem, thanks to `gofmt` and in broader context [golangci-lint](https://golangci-lint.run/usage/linters/) with all its integrated linters.

But Python world has started catching up as well, there is [Pylama](https://github.com/klen/pylama) which also integrates with various linters / checkers, and of course there is [Black](https://black.readthedocs.io/en/stable/) for formatting the code.

The sane thing to do is make sure this tools are run on save in your IDE or editor of choice. The bare minimum would be running them as part of the build, or as [Git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks), or even better all three!

Using this tooling you will not only solve most style discussions, but also aviod many scenarios that result in inferior code.

That said, keep in mind that when one knows what they are doing, one is not obliged to follow all the suggestions to the letter, for example Pylama [allows enabling or disabling specific features of linters](http://klen.github.io/pylama/#configuration-file), for the ones that are configurable.



### Update it

This service has significant number of direct dependencies, and even larger number of transitive ones, you can view the whole tree using `poetry show --tree`, Here is example output, with extra newlines between modules added for clarity:

```zsh
% poetry show --tree
black 22.3.0 The uncompromising code formatter.
├── click >=8.0.0
│   └── colorama *
├── mypy-extensions >=0.4.3
├── pathspec >=0.9.0
├── platformdirs >=2
└── tomli >=1.1.0

fastapi 0.75.2 FastAPI framework, high performance, easy to learn, fast to code, ready for production
├── pydantic >=1.6.2,<1.7 || >1.7,<1.7.1 || >1.7.1,<1.7.2 || >1.7.2,<1.7.3 || >1.7.3,<1.8 || >1.8,<1.8.1 || >1.8.1,<2.0.0
│   └── typing-extensions >=3.7.4.3
└── starlette 0.17.1
    └── anyio >=3.0.0,<4
        ├── idna >=2.8
        └── sniffio >=1.1

httpie 3.1.0 HTTPie: modern, user-friendly command-line HTTP client for the API era.
├── charset-normalizer >=2.0.0
├── colorama >=0.2.4
├── defusedxml >=0.6.0
├── multidict >=4.7.0
├── pygments >=2.5.2
├── requests >=2.22.0
│   ├── certifi >=2017.4.17
│   ├── charset-normalizer >=2.0.0,<2.1.0
│   ├── idna >=2.5,<4
│   ├── pysocks >=1.5.6,<1.5.7 || >1.5.7
│   └── urllib3 >=1.21.1,<1.27
└── requests-toolbelt >=0.9.1
    └── requests >=2.0.1,<3.0.0
        ├── certifi >=2017.4.17
        ├── charset-normalizer >=2.0.0,<2.1.0
        ├── idna >=2.5,<4
        ├── pysocks >=1.5.6,<1.5.7 || >1.5.7
        └── urllib3 >=1.21.1,<1.27

hypothesis 6.44.0 A library for property-based testing
├── attrs >=19.2.0
└── sortedcontainers >=2.1.0,<3.0.0

mypy 0.942 Optional static typing for Python
├── mypy-extensions >=0.4.3
├── tomli >=1.1.0
└── typing-extensions >=3.10

pycodestyle 2.8.0 Python style guide checker

pyflakes 2.4.0 passive checker of Python programs

pylama 8.3.8 Code audit tool for python
├── mccabe >=0.6.1
├── pycodestyle >=2.8.0
├── pydocstyle >=6.1.1
│   └── snowballstemmer *
└── pyflakes >=2.4.0

pylint 2.13.7 python code static checker
├── astroid >=2.11.3,<=2.12.0-dev0
│   ├── lazy-object-proxy >=1.4.0
│   └── wrapt >=1.11,<2
├── colorama *
├── dill >=0.2
├── isort >=4.2.5,<6
├── mccabe >=0.6,<0.8
├── platformdirs >=2.2.0
└── tomli >=1.1.0

pytest 7.1.1 pytest: simple powerful testing with Python
├── atomicwrites >=1.0
├── attrs >=19.2.0
├── colorama *
├── iniconfig *
├── packaging *
│   └── pyparsing >=2.0.2,<3.0.5 || >3.0.5
├── pluggy >=0.12,<2.0
├── py >=1.8.2
└── tomli >=1.0.0

requests 2.27.1 Python HTTP for Humans.
├── certifi >=2017.4.17
├── charset-normalizer >=2.0.0,<2.1.0
├── idna >=2.5,<4
├── pysocks >=1.5.6,<1.5.7 || >1.5.7
└── urllib3 >=1.21.1,<1.27

structlog 21.5.0 Structured Logging for Python

uvicorn 0.17.6 The lightning-fast ASGI server.
├── asgiref >=3.4.0
├── click >=7.0
│   └── colorama *
└── h11 >=0.8
```

Any of these can go out of date, become vulnerable, become unusable with a newer version of Python and so on. Thus it is important to keep the dependency tree up to date! Thankfully helpful tooling exists, especially for projects hosted on GitHub, have a look at [how to have the versions updated automatically](https://github.blog/2020-06-01-keep-all-your-packages-up-to-date-with-dependabot/), also [official documentation](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuring-dependabot-version-updates#enabling-github-dependabot-version-updates).

This project includes a `dependabot.yml` configured for Poetry and Docker, for more infromation you can view detailed [configuration options for Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file).

Thanks to this your project will receive automatic pull requests when updates are availalbe!

Of course, it is important to have proper testing in place for these pull requests, without automated testing this can become very hard to manage.

To avoid dependency hell, a good strategy is to keep your dependencies minimal, updating the language runtime with it the standard library is significantly easier than updating the whole dependency graph. It is OK to take the easy path as a beginner and just use the libraries, but as one learns and grows it is important to understand that dependencies are rarely optimized for _your specific usecase_. It is important to _know what your specific use case is_ and then to judge whether implementing something that solves it 100% for you, not 80% or 200%, will result in simpler code, fewer dependencies, easier long term maintenance and so on.

This practice is unfortunately rarely followed in Python, but it is [pretty popular in Go](https://go.dev/doc/articles/wiki/). This has also to do with the fact that [Go](https://pkg.go.dev/std) and [Python](https://docs.python.org/3/library/) standard libraries have very different focus. This is alright, the languages are different, and a thing that is idiomatic in one language is not neccessarily in another.

Speaking of standard libraries, reading the code in them is a good way to learn about the language, but one has to have some caveats in mind. For example Python standard library uses `unittest` for testing, simply because it is a built-in, but Pytest isn't. This does not mean you should use unittest in your own code! on the other hand Go standard library's `testing` package is widely adopted in the ecosystem, and although wrappers exist they all integrate with it.



### Secure it

Dependabot [can help](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/configuring-dependabot-security-updates) with security updates as well. I would highly recommend using it. We do for this repository.

There are other options available too, for exmaple the popular [Semgrep](https://semgrep.dev), [Snyk](https://snyk.io), and others.



### Package it

Alright, so we comitted, tested, updated, secured, whatnot.. time to package the application! for example build the Docker image and push it to a registry. [GitHub Actions](https://github.com/features/actions) is a great way to do this, it supporst [reusable workflows](https://github.blog/2021-11-29-github-actions-reusable-workflows-is-generally-available/), and there is integration with almost everything. It is not overly expensive nor excessively broken.

There are too many other options to mention, I will just say that if you are using a cloud, you should probably also look into build/deployment services offered by that cloud, for example [Google Code Build](https://cloud.google.com/build) and [Google Cloud Deploy](https://cloud.google.com/deploy) for [GCP](https://cloud.google.com).

We do not touch the subject of Build systems such as [Bazel](https://bazel.build), [Buck](https://buck.build) etc. or other more complicated topics such as monorepos here.



### Host and deploy it

All that is fine and good, but where do we host it?



#### VPS

Just run [Watchtower](https://containrrr.dev/watchtower/) on a VPS, such as [AWS LightSail](https://aws.amazon.com/lightsail/) or many other, and usually cheaper, options such as [Scaleway](https://www.scaleway.com) or [Linode](https://www.linode.com) and completely avoid the need to deploy anything! the container will simply restart when there is a new image in the registry.



#### Deploy to AWS Lambda

AWS is the elephant int the cloud room, it would be amiss not to mention a few options of deploying there.

[Creating](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html) and [Deploying](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/deploy-lambda-functions-with-container-images.html) a container to Lambda has been long supported.

[AWS ECS](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-steps-ecs.html) is also an option.



#### Deploy it somewhere else

These days there are amazing services available that present you will a whole toolset for developing modern web applications. For just a few great examples you can look at [Fly](https://fly.io) and [Netlify](https://netlify.com).



### Put a badge on it

It is nice to see the status of build, code, compliance and so on right on the project's GitHub landing page, so use [shields.io](https://shields.io) to add badges to your project README.md.



## That is all folks

If you have suggestions, questions, or any other queries - You can open an issue on this repo, or send a PR.

Thanks and good luck!



## Opportunities for improvement

TODO: Test the reports module.

TODO: Do something more interesting and meaningful than fetching stock info, which one can easily do directly.

TODO: Make this properly production ready.

TODO: Include more information about what professional hosting for this might look like.

TODO: Add distributed tracing support.

TODO: Consider caching API requests in the database.

TODO: Improve the tests, there is a lot of room for refactoring.

TODO: Add more comments.

TODO: Improve README, CONTRIBUTING, the CLA etc.

TODO: Figure out why mock is creating files in the project directory when running pytest.

TODO: Improve Dockerfile


## How to run stuff

Clone it, then install and test:

```zsh
poetry install

poetry run pytest -vv --cov
```

To run the app cd into the project directory and:

```zsh
poetry run uvicorn pyapid.api:app --reload
```

If you want multiple workers append `--workers 4` to that or similar.


To build with Docker simply cd into the project directory and:

```zsh
docker build . -t pyapid:latest
```

To run the resulting image:

```zsh
docker run pyapid:latest
```

You can append arguments to that, they will get passed to `uvicorn`. Look in `Dockerfile` for more hints.
