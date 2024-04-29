<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Email][email-shield]][email-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://prempredict.mtlh.dev/">
    <img src="https://prempredict.mtlh.dev/static/prem_logo.svg" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">PremPredict</h3>
  <h4 align="center">
    <a href="https://prempredict.mtlh.dev/">Live Demo</a>
  </h4>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

PremPredict is a project aimed at people with a distinct interest in premier league predictions, using an advanced learning algorithm analysis, players will compete against the algorithm and other users across a full season. Scoring points for every correct prediction; combined into an overall leaderboard and private leagues like those used in fantasy football applications. The goal is that by referencing an accurate model, users will make more informed decisions than other platforms. Providing a fun interactive interface suitable for all devices through a public website. 

<h2 align="center">
  <img src="https://www.mtlh.dev/assets/prempredictions_thumb.b7a11329_Z26hoIb.webp" alt="Thumbnail" width="60%" height="60%">
</h2>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

#### Frontend 
<table>
  <thead>
		<td>
			<b>HTML</b>
		</td>
		<td>
			<b>Tailwind CSS</b>
		</td>
    <td>
			<b>Javascript</b>
		</td>
    <td>
			<b>HTMX</b>
		</td>
	</thead>
  <tr>
    <td align="center">
      <a href="https://developer.mozilla.org/en-US/docs/Web/HTML">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" alt="HTML" width="80" height="80">
      </a>
    </td>
    <td align="center">
      <a href="https://tailwindcss.com/">
        <img src="https://static-00.iconduck.com/assets.00/tailwind-css-icon-2048x1229-u8dzt4uh.png" alt="Tailwind" width="80" height="80">
      </a>
    </td>
    <td align="center">
      <a href="https://developer.mozilla.org/en-US/docs/Web/javascript">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" alt="JS" width="80" height="80">
      </a>
    </td>
    <td align="center">
      <a href="https://htmx.org/docs/">
        <img src="https://www.alchemists.io/images/projects/htmx/icon.png" alt="HTMX" width="80" height="80">
      </a>
    </td>
  </tr>
</table>

#### Backend
<table>
  <thead>
		<td>
			<b>Python</b>
		</td>
		<td>
			<b>Django</b>
		</td>
    <td>
      <b>CockroachDB</b>
    </td>
    <td>
      <b>Vercel</b>
    </td>
    <td>
      <b>Cron-Job.org</b>
    </td>
	</thead>
  <tr>
    <td align="center">
      <a href="https://www.python.org/">
        <img src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png" alt="Python" width="80" height="80">
      </a>
    </td>
    <td align="center">
      <a href="https://www.djangoproject.com/">
        <img src="https://static-00.iconduck.com/assets.00/django-icon-1606x2048-lwmw1z73.png" alt="Django" width="80" height="80">
      </a>
    </td>
    <td align="center">
      <a href="https://www.cockroachlabs.com/">
        <img src="https://cdn.worldvectorlogo.com/logos/cockroachdb.svg" alt="CockroachDB" width="80" height="80">
      </a>
    </td>
    <td align="center">
      <a href="https://vercel.com/">
        <img src="https://cdn.changelog.com/uploads/icons/news_sources/qGw/icon_large.png?v=63692097118" alt="Vercel" width="80" height="80">
      </a>
    </td>
    <td align="center">
      <a href="https://cron-job.org/en/">
        <img src="https://cdn1.iconfinder.com/data/icons/cloud-hosting/32/stopwatch-icon-512.png" alt="Cron-Job.org" width="80" height="80">
      </a>
    </td>
  </tr>
</table>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

If you wish to clone and run the repo, please follow the steps below.

### Installation

1. Clone the repo

```sh
git clone https://github.com/mtlh/FinalYearProject_PremPredict.git
```

### Run Commands

Please refer to readme files in the frontend and predictionmodel folders for setup since they are independently managed.

## Limitations

* <a href="https://cockroachlabs.cloud/clusters">CockroachDB</a> - 50 million request usage per calender month.
* <a href="https://vercel.com">Vercel</a> - Function duration 100 GB-Hours per calender month.

### Data Sources

* https://www.football-data.org/ - Team Standings & Fixtures
* https://www.fotmob.com/ - Team Logos
* https://fantasy.premierleague.com/ - Deadlines
* https://www.football-data.co.uk/downloadm.php - Seasonal Spreadsheets

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] /
  - [x] Core functionality
  - [x] Add styling
  - [x] Review code

- [x] /scores
  - [x] Core functionality
  - [x] Add styling
  - [x] Review code

- [x] /predict
  - [x] Core functionality
  - [x] Add styling
  - [x] Review code

- [x] /table
  - [x] Core functionality
  - [x] Add styling
  - [x] Review code

- [x] /leaderboard
  - [x] Core functionality
  - [x] Add styling
  - [x] Review code

- [x] /profile
  - [x] Core functionality
  - [x] Add styling
  - [x] Review code

Last updated 26/04/2024

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments 😎

Some resources that I have read/used that I think are useful to share:

* [GitHub Pages](https://pages.github.com)
* [Vercel Hosting](https://vercel.com/)
* [Readme Template](https://github.com/othneildrew/Best-README-Template)
* [Markdown Guide](https://www.markdownguide.org/basic-syntax/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-blue.svg?style=for-the-badge&logo=linkedin
[linkedin-url]: https://linkedin.com/in/mtlh

[email-shield]: https://img.shields.io/badge/-Email-blue.svg?style=for-the-badge&logo=microsoftoutlook
[email-url]: mailto:P2590750@my365.dmu.ac.uk