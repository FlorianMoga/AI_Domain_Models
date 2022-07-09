
# Domain Model enabled AI Algorithms

This repo has the goal of streamlining a way to transform invoices into domain models. For that it uses an frontend component for ingesting the invoices in pdf or image format and a backend component to handle all the processing  and conversion.




## Frontend

The app is written in Flutter. It provieds three pages in a menu:
- Home page, where you can enter a new domain model or populate an existing one. after creating a new DM it will not dynamically be added to the existing models cards
- Domain Models, where it will be displayed the link provided for the Domain Models visualisation
- Initialize page, where one can enter the link for the backend access, the token needed for the GEP Domain Model creation tool and the link to the website displaying the Domain Models created


## Backend

It has four parts:
- the main file present in the root folder, containing the Flask component that exposes the token retrieval endpoint and the invoice file retrieval endpoint
- the main file present in the frontend/straighten_image subfolder, that straightens the image and gives it an A4 aspect ration
- the main file present in the backend/extract_table subfolder using hardcoded data from the Jupiter notebook found in the same folder
- the main file present in the backend/extract_text subfolder, that calls on all the methods to trsnpose the information from the invoice file into data in a TXT and JSON format, output files found in their respective folders


## Run Locally

Clone the project

```bash
  git clone https://github.com/floriankpq/AI_Domain_Models
```

Go to the project directory

```bash
  cd AI_Domain_Models
```


**Backend**

Go to the backend directory

```bash
  cd AI_Domain_Models/backend
```

Change all Paths to your specific case.

Install dependencies

```bash
  npm install requirements.txt
```

Go to the root directory

```bash
  cd AI_Domain_Models
```

And start the main.py .
You will soon get to see a line in the terminal similar to "" 

Use ngrok(https://ngrok.com/download) to forward localhost

```bash
  cd %ngrok folder typically C:\ProgramData\chocolatey\bin%
```

And start the service
```bash
  ngrok http %flask port usually 8000%
```

**Frontend**

Go to the frontend directory

```bash
  cd AI_Domain_Models/frontend
```

Install dependancies
```bash
   flutter pub get
```

Use Android Studio's Virtual Device Manager to create a new device.
After its creation, press the play button to start it.

Go to your IDE and run the app inside the Virtual Device.
For example in Intellj the IDE will autmoatically detect the virutal device, so you have to just press play.

Inside the app initialize all the values.

You're done 👌





## Features

- Pdf and image inputs
- Image preprocessing
- Logo and table detection
- Text extraction algorithms
- Results to JSON and Domain Model generator API calls converters


## Tech Stack

**Client:** Flutter

**Server:** Python


## API Reference

#### **Get invoice**

```http
  POST /upload
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file`    | `multipart-file` | **invoice file** |

#### **Set token**

```http
  POST /token
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`   | `string` | **value of access token**         |



## Roadmap

- Filling the Domain Model with runtime data from our already generated JSON files

- Implementing our own Deep Learning algorithm for table recognition and tabular data extraction

- Using a NLP technique for text processing 

- Logo recognition via Deep Learning or Reverse Image search

- Predicting values for an invoice based on custom fields and invoice type


## Authors

- **[@floriankpq](https://www.github.com/floriankpq)**
- **[@coto24](https://github.com/coto24)**
- [@includeSimon](https://github.com/includeSimon)

