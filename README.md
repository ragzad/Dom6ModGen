# Dominions 6 AI Mod Generator

## Project Purpose

This Django-based full-stack web application enables users to collaboratively design and generate complete *Dominions 6* mods. By combining AI-generated `.dm` files and sprites with user-contributed data, this tool creates a growing repository of community-driven mod content. The application allows users to input, edit, and browse unit, faction, spell, and item data - all stored in a relational database and used to generate mods.

This satisfies the MS3 project requirement to:
- Build a relational database-backed application
- Enable full CRUD functionality
- Offer practical and creative value to a real-world community

---

## Value Provided

- **Community Collaboration**: Users can contribute their custom unit and nation designs, helping to grow a public collection of high-quality, ready-to-use Dominions mods.
- **Automation**: AI models generate `.dm` mod scripts and unit sprites based on user input, reducing technical barriers.
- **Utility for Modders**: Beginners and veterans alike can easily create and download full mods without writing any code.
- **Educational Value**: The site owner (and users) deepen their understanding of data modeling, game balance, and full-stack development using modern web tools.

---

## Technologies Used

| Layer           | Stack                                                   |
|----------------|----------------------------------------------------------|
| Backend         | Python + Django                                          |
| Frontend        | HTML, Custom CSS, JavaScript (optionally Bootstrap)     |
| Database        | PostgreSQL (or MySQL)                                    |
| AI Integration  | OpenAI GPT-4 or Claude 2 (via API) for mod generation   |
| Image Gen       | Stable Diffusion (via API or Hugging Face endpoint)     |
| Hosting         | Deployed to Heroku (or Render/Vercel/DjangoAnywhere)    |
| Version Control | Git + GitHub                                             |

---

## Features & Requirements Fulfilled

| Requirement                     | Implementation                                                                 |
|--------------------------------|----------------------------------------------------------------------------------|
| **Data Handling**              | Stores units, nations, spells, and items in a relational PostgreSQL database    |
| **Database Structure**         | Well-structured models using Django ORM, with clear entity relationships         |
| **CRUD Functionality**         | Users can Create, Read, Update, and Delete all mod elements via the UI          |
| **HTML + CSS Frontend**        | Hand-written HTML templates and custom CSS for layout and styling               |
| **Structured Layout**          | Includes Bootstrap-powered navigation and responsive layout                      |
| **README.md**                  | You're reading it                                                             |
| **Version Control**            | GitHub repo with clearly separated commits and tracked progress                  |
| **Attribution**                | All AI models and external sources are cited in comments and this file           |
| **Deployment**                 | App will be deployed on Heroku (free tier, PostgreSQL add-on)                    |
| **Security**                   | Environment variables for API keys, no secrets committed                         |

---

## Database Schema

Here is a visual representation of the application's database schema:

![Database Schema](Dom6ModGen\DBSchema\db_schema_manual.png)
