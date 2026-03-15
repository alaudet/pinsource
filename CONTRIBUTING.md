# Contributing Guidelines for pinsource

Contributions are welcome.

1. Please open an issue in the tracker to suggest a change or fix before issuing the pull request.

2. All pull requests should target the `devel` branch and not `main`.

3. All code submitted must be your own or be allowable to redistribute under the Apache 2.0 License.

4. Follow PEP 8 guidelines for code style. Follow PEP 257 for docstrings — add a docstring to every function so others understand its purpose. Add comments where the intent is not immediately obvious. Code that is difficult to read will not be accepted.

5. New functionality must include a unittest. All existing tests must pass before issuing a pull request. Run the test suite with `pytest tests/` and confirm a clean result. See `tests/README.md` for details.

6. New Python dependencies must be added to `debian/control` as well as the code. Contributions must not break the `.deb` build (`dpkg-buildpackage -us -uc -b`).

7. I can't promise that all new features will be accepted. However, the Apache 2.0 license allows and welcomes you to fork the code and release an altered version under any compatible license. Please review the requirements of the Apache 2.0 license when doing so.

8. You may use AI assistants (such as Claude) to help write code. Be honest about your usage. Do not submit code you do not understand or that has no clear purpose. If the intent is unclear or it does not benefit the application, it will not be accepted.

9. If you want to contribute, join the Discord group for Raspi-Sump — there are `#code-discussion` and `#pinsource` channels. It is not mandatory but makes collaboration much easier. Email [alaudet@linuxnorth.org](mailto:alaudet@linuxnorth.org) to request an invite link.
