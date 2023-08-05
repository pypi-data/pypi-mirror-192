# Magic Key

This module provides iPython integration and magics that allow exact, inexact and intellegent code execution.


Example. In the context of the text interface, the following is available:
```
    >>> @`merlin.name`      #names
    Myrddin Wyllt

    >>> @merlin Please, can you remind me, what is your first name?  It's M... ?
    It's Merlin.

    >>> @`merlin.first_name()`
    AttributeError: 'Person' object has no attribute 'first_name'

    >>> @*`merlin.first_name()`
    Unavailable. Try: .name

    >>> @`merlin.name.split()[0]`
    Myrddin

    >>> @```merlin.name.split()[0]```
    Myrddin

    >>> #names?
    @`merlin.name` Myrddin Wyllt
```

Using the following rules:
    * Strings starting with %, @, #, ?, * are translated to iPython magics. 
    * Code in the codeblocks prefixed by @ is executed in iPython
    * Prompts directed to objects prefixed by @ is executed by magic
    * Prompts directed to objects prefixed by @ is executed by magic
    * Code in the code blocks prefixed by @* is executed by magic
    * Rest is being passed through (text, code blocks)
    * The ASCII code of * asterisk is obviously 42



Example:
```
    >>> import magic_key
    >>> from .examples.person import Person               # Classic Person class example

    >>> merlin = Person("Myrddin Wyllt", 42, "Caledonia") 

    >>> magic_key.insert_into(engine)
    >>> magic_key.turn_on(merlin, magic_type = None)      # Using the default iPython matching engine
    >>> merlin.name()
    Myrddin Wyllt

    >>> @merlin What is your first name?
    Invalid .. .  # TODO add actual error

    >>> 
    >>> magic_key.turn_on(merlin, magic_type = False)      # Using the search engine
    >>>
    >>> @merlin Please, can you remind me, what is your first name?  It's M... ?
    About 1 search result(s):
        Myrddin

    >>> merlin.first_name()                             
    Invalid... About 1 search result:                    # Note, it expects you to learn
        .name() - docstring                            

    >>> 
    >>> magic_key.turn_on(merlin, magic_type = True)      # Using the intellegence engine
    >>>
    >>> @merlin Please, can you remind me, what is your first name?  It's M... ?
    It's Merlin.

    >>> merlin.first_name()                             
    Unavailable. Try: .name() - docstring                 # Note, it expects you to learn

    >>>  
```




How does it work?  Well, the short answer is - magic. The long answer involves a lot of
math, code, multidimensional spaces and some theoretical findings that are generally
attributed to a French Baron, named Augustin-Louis Cauchy who had lived during the Age
of Enlightenment. Paradoxely, one could think that it doesn't work. Only that it does,
with the help of magic.

This module focus is on the magic key aspect of code execution, separate from the magic
engine aspect of it and follows the bring-your-own-magic-engine philosophy. The name of
the module was inspired by the children's fable The Toy Robot, by an Unknown author of
Ladybird Books, first published in 2010. It is a recommended read for any aspiring 
intellegent code execution practitioner. 

## Getting started


TODO: Pydantic types?


To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Install

```
pip install magic-key
```

## Integrate with your tools


## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thank you to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README
Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
The project is accepting Apache 2.0 compatible contibutions. Please refer to CONTRIBUTING.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
This project is maintained by [Round Table Game community](https://roundtable.game), an unincorporated
association of: an anonymous Delaware company (registered to conduct business in California) and an anonymous
AI Safety nonprofit organization, as well, registered in California.

So far, the major contributors to this project prefer to remain anonymous and act as Merlinus Caledonensis.

## License
The project license is Apache 2.0.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
