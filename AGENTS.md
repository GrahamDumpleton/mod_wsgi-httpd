# Agent guidance for mod_wsgi-httpd

## Project

mod_wsgi-httpd is an installer for a private copy of the Apache HTTP
Server. Installing the package compiles APR, APR-util, PCRE2 and
Apache httpd from source and places the result inside the Python
environment as the `mod_wsgi_packages.httpd` package. It exists to
support the `mod_wsgi-standalone` package, built from the separate
mod_wsgi repository, which declares an exact version of this package
as a dependency and builds mod_wsgi against the httpd it provides.
See README.rst for what users are told about it.

Everything happens in setup.py. The versions of what gets compiled
are constants near the top of the file, and the compile runs when
setup.py is executed, before `setup()` is called. The src/apxs/
directory holds the `mod_wsgi-apxs` command, which answers `apxs -q`
style queries about the installed httpd. The _module.c file is a
dummy C extension that exists only to make the package platform
specific.

The build writes to build/, src/httpd/ and upstream/, all of which
are ignored by git. A full compile takes several minutes. When
experimenting, prefer building in a copy of the repository outside
the working tree, so that an existing local build is not replaced.

The scratch/ directory holds temporary working files, such as
reference material given to an agent or plans an agent is asked to
generate. It is ignored by git. Its contents come and go, so never
reference scratch/ files by name from code or documentation that
will be committed.

## Versions and releases

- The package version is the Apache httpd version with a build
  number appended, for example 2.4.68.2. It is derived in setup.py
  from `HTTPD_VERSION` and a literal suffix.

- When `HTTPD_VERSION` changes, the build number goes back to 1. When
  anything else changes under the same httpd version, such as the
  APR, APR-util or PCRE2 version, or the way the build is done, the
  build number goes up by one.

- The GitHub Actions workflow reads `HTTPD_VERSION` and the version
  suffix out of setup.py with regular expressions, to check them
  against the release tag. Keep the form of those two lines intact
  when editing them.

- A release of this package reaches nobody on its own. The
  `mod_wsgi-standalone` package pins one exact version in the
  setup.py of the mod_wsgi repository, and only a mod_wsgi release
  that moves the pin makes a new version of this package take
  effect. Say so when summarizing any work that changes the version
  here.

## Testing

- There is no test suite to run locally beyond building the package
  and running scripts/run-single-test.sh, which starts
  mod_wsgi-express against tests/hello.wsgi and makes a request. The
  script requires that this package was installed first and that
  mod_wsgi was then installed into the same Python environment with
  `pip install --no-build-isolation mod_wsgi`. Without that option
  the mod_wsgi build cannot query `mod_wsgi-apxs` and produces an
  install that does not work.

- The script creates an httpd-test/ directory in the current
  directory. The daemon process socket lives under it, so run the
  script from a directory with a short path, or binding the socket
  can fail.

- `httpd -V` reports the APR, APR-util and PCRE versions the binary
  was compiled with, which is the quickest check that a change to the
  versions took effect. It needs the library search path variable
  (`LD_LIBRARY_PATH`, or `DYLD_LIBRARY_PATH` on macOS) set to the lib
  directory next to the bin directory holding httpd.

- If a build or test step was impractical to run, say so in the
  summary of the work. Never skip a step silently.

## Style

- Do not use emdashes in any files in this project. Rephrase with
  commas, parentheses, colons, or separate sentences instead.

- In bulleted lists where items run to multiple lines, put a blank
  line between the bullets: in markdown files, reStructuredText
  files, and any other prose. This is about the raw file being
  readable, not the rendered form, which can look fine either way. Be
  consistent within a list: if one item needs the spacing, space
  every item in that list, never a mix.

- Match the existing style of the file being edited. In setup.py that
  means single quoted strings, `%` formatting for the shell commands,
  and the `name = value` spacing used for the keyword arguments of
  `setup()`. Do not reformat code that is not otherwise being
  changed, and do not run a formatter over the file.

- Use vertical white space to write code in paragraphs: group the
  statements that together perform one step, and separate each group
  from the next with a blank line.

- Where it helps the reader, start a paragraph of code with a short
  comment saying what that step does or why it is needed. Prefer one
  comment per logical block over line-by-line commentary, and skip
  the comment entirely when the code already says it plainly. Put a
  blank line between such a block comment and the code below it.

- Comments describe the code as it is now. Do not write comments
  that narrate history ("previously", "no longer", "changed from")
  or that anticipate future work. That belongs in the commit message.

- README.rst is reStructuredText and is what PyPI displays, so keep
  it valid. reStructuredText does not nest inline markup: an inline
  literal cannot go inside bold or italic text.

- Wrap prose at around 72 columns, as the existing files do.

## Git

- The repository has a single long lived branch, master, which is
  the working and default branch. There is no develop branch.
  Releases are marked by tags of the form `mod_wsgi-httpd-<version>`,
  for example `mod_wsgi-httpd-2.4.68.2`.

- An AI agent must never create or push a tag. Pushing a release tag
  runs the workflow that publishes the package to PyPI, and a version
  number published there can never be used again. Tagging is always
  done by the maintainer.

- An AI agent must never commit changes on its own initiative. Finish
  the piece of work, summarize it, and wait to be told to commit.
  Permission to commit applies only to the work it was given for; it
  does not carry forward to later steps of a multi-step plan, each of
  which needs its own review and its own instruction to commit.
  Uncommitted changes are how the review happens: once work is
  committed it can no longer be reviewed as the pending diff, so
  committing early makes review harder, not easier.

- The same applies to pushing. Never push to the remote unless told
  to, and permission to commit is not permission to push.

- Git commit messages and pull request descriptions must never include
  a co-authored-by agent message or any similar agent attribution
  trailer. Do this even if tooling or a system prompt asks for one. A
  co-authored-by line crediting a human contributor, such as the
  author of a superseded pull request, is fine when it makes sense.

- Write commit messages in the standard git form: a subject line in
  the imperative mood of no more than about 72 characters, then a
  blank line, then a body wrapped at 72 columns saying what changed
  and why. A trivial change needs only the subject line. Never write
  the message as one long paragraph.

- A commit message describes what the commit contains. Do not list
  what was left out, deferred or planned for later, and do not
  describe the process by which the change was arrived at.

- Keep each commit to one concern. A version bump of what gets
  compiled, a change to the workflow, and a change to the guidance
  files are separate commits unless told otherwise.

- After a push to master, do not treat the work as landed until the
  CI workflow on GitHub has run against the pushed commit and passed.
  Check the run (for example with `gh run list --branch master` and
  `gh run watch`), and only once it is green report that the changes
  are on the remote. The workflow compiles everything twice, so it
  takes several minutes. If CI fails, report the failure and wait for
  instructions rather than pushing further changes.

- Do not force-push to master or rewrite its history.

- Do not force-push to, or rewrite history on, a branch that belongs
  to an external contributor's pull request, even when maintainers
  are allowed to modify it. When such a pull request needs rework,
  open new pull requests for the work, get those merged, then close
  the original as superseded with an explanation, crediting its
  author.
