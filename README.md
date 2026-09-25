# Kevin Abijuru's Portfolio

A personal portfolio website that presents who I am, the skills I work with and the projects I have built. It is a
static, responsive site written in HTML and Bootstrap CSS, developed continuously with Git and published on GitHub
Pages as part of the DevOps course at Saint Joseph Integrated Technical College (SJITC).

## Features

- **About me section:** a short introduction with my profile photo, my background in software development and
  my current focus on DevOps.
- **Skills & focus areas section:** the technologies and practices I work with, such as software development,
  Bluetooth-based systems, HTML5 & CSS3, Bootstrap, Git & GitHub and continuous development and integration.
- **Projects section:** project cards that show the description, deliverable, duration, role, status and budget of
  each project, currently the *Student Attendance System* and this *Personal Portfolio Website*.
- **Contact section:** a link to my GitHub profile.
- **Responsive layout:** the page adapts to phones, tablets and desktops, and uses semantic HTML with accessible
  colour contrast.
- **License information:** the MIT License and third-party notices are provided in [LICENSE.txt](LICENSE.txt).

## How to run this project

The portfolio is already running online, so you can view it without installing anything:

**Live site:** <https://kevinabijuru.github.io/>

To run your own copy locally, follow the steps below. There is no build step and there are no dependencies to
download, because Bootstrap is bundled in `styles/main.css`.

### Prerequisites

- A modern web browser such as Chrome, Edge, Firefox or Safari.
- [Git](https://git-scm.com/downloads) to clone the repository.
- *Optional:* [Node.js](https://nodejs.org/) (for `npx serve`) or [Python 3](https://www.python.org/downloads/)
  (for `python -m http.server`) if you prefer to view the site through a local web server instead of opening the
  file directly.

### Installation

1. **Clone the repo:** run the command

   ```bash
   git clone https://github.com/KevinAbijuru/kevinabijuru.github.com.git
   ```

2. **Go into the project folder:**

   ```bash
   cd kevinabijuru.github.com
   ```

3. **Open the portfolio.** Choose one of these options:
   - Double-click `index.html`, or open it from your browser with *File > Open file*.
   - Or start a local web server and open <http://localhost:8000>:

     ```bash
     python -m http.server 8000
     ```

     (or `npx serve .` if you use Node.js, which prints its own address)

4. **Make and publish your changes.** Edit `index.html` or `styles/custom.css`, then commit and push. GitHub Pages
   republishes the site automatically after each push:

   ```bash
   git add .
   git commit -m "Describe what you changed"
   git push origin main
   ```

## Project structure

```text
kevinabijuru.github.com/
├── index.html          # The portfolio page (about, skills, projects, contact)
├── images/
│   └── avatar.jpg      # Profile photo
├── styles/
│   ├── main.css        # Bootstrap v4.4.1 (third-party)
│   └── custom.css      # Portfolio-specific styles
├── LICENSE.txt         # License breakdown
└── README.md           # This file
```

## Built with

- HTML5
- CSS3 and [Bootstrap 4.4.1](https://getbootstrap.com/docs/4.4/)
- [Git](https://git-scm.com/) and [GitHub](https://github.com/) for version control
- [GitHub Pages](https://pages.github.com/) for hosting

## License

The source code and written content of this project are released under the **MIT License**, which lets you use,
copy, modify and share them as long as you keep the copyright notice. Two parts of the repository are **not** covered
by that grant:

- `styles/main.css` is Bootstrap v4.4.1, which has its own MIT license and copyright notice.
- `images/avatar.jpg` is a personal photo of the author and is **all rights reserved**. Please do not reuse it
  without written permission.

The project was created for educational purposes as part of a continuous assessment at SJITC. See
[LICENSE.txt](LICENSE.txt) for the full breakdown and license texts.

## Contributors

- **Kevin Abijuru** ([@KevinAbijuru](https://github.com/KevinAbijuru)): author and maintainer.

## Acknowledgements

- The [Bootstrap](https://getbootstrap.com/) authors for the CSS framework.
- Saint Joseph Integrated Technical College (SJITC) for the DevOps course and assignment brief.

## Project link

Project Link: <https://github.com/KevinAbijuru/kevinabijuru.github.com>
