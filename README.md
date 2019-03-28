# Student Organizational System

This is the source code for the Student Organizational System, a project by Thomas Patton and Andres Beltran for EECS 393. The goal of the project is to create a system for students in a university to meet for classes. We found that students at university often did not have the proper resources to easily meet with classmates. As a result, we built a website with Python and Django to facilitate this. Registered users have the ability to create meetings for classes and quickly share them with their friends. For a more in-depth look at the purpose of this project, see the Software Requirements Specification document and the Design Document.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Your computer will need to have Python. A good explanation of how to do this is available on the [Python Website](python.org).

From there, you will need to install a few packages. To handle the website framework, you will need to download Django.

```
$ pip install Django
```

To handle the form tags used, install crispy-forms

```
$ pip install --upgrade django-crispy-forms
```

And lastly to handle the images, you will need Pillow

```
$ pip install Pillow
```

## Documentation

See the Wiki files in the repository for a more in depth look at the roadmap of the project and the most recent documentation. This includes our Software Requirements Specification, Testing Documents, and our Design Document.

## Built With

Our application is primarily built with Python 3.6 using the Django Framework. For the frontend, we used a combination of HTML, CSS, Javascript, and Bootstrap.

The program was primarily developed in PyCharm, with the assistance of Git.

## Authors

* **Andres Beltran** - *Backend Development Engineer* - [GitHub](https://github.com/andresbeltran98)
* **Thomas Patton** - *Backend Development Engineer* - [GitHub](https://github.com/thomaspttn)

A thanks is also due to Corey Shafer, for his instructional guides on learning the Django framework.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
