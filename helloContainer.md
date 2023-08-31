# Comprehensive Guide to Building and Deploying a Flask and scikit-learn Application in a Docker Container

The guide outlines a comprehensive process to build and deploy a machine learning application using Flask and scikit-learn, packaged in a Docker container. It is broken down into three main parts:

1.  Creating a Flask Application with scikit-learn Model:
    
    -   First, you initialize a Python project and create a virtual environment.
    -   Next, you build a Flask app and train a scikit-learn model.
    -   The model is then loaded into the Flask app and several endpoints (e.g., for predictions and metadata) are created.

2.  Containerizing the Flask Application with Docker:
    
    -   You install Docker and its dependencies on your machine.
    -   A Dockerfile is created to package your application.
    -   You then build and run a Docker container based on this Dockerfile.

3.  Testing and Deployment:
    
    -   The Flask routes are tested to make sure they work as expected.

Throughout the guide, code snippets and commands are provided for clarity, including Python code for the Flask app and Docker commands for container operations.

# 1: Create a Flask Application with scikit-learn Model

1.1.  **Initialize a New Python Project**: 

- Create a python virtual env and a source folder. Create a `requirements.txt` to list the Python packages you'll need (Flask, scikit-learn, etc.).
    
        python -m venv helloContainerWithFlaskAndScikitLearnApp
        
        mkdir helloContainerWithFlaskAndScikitLearnWS && cd helloContainerWithFlaskAndScikitLearnWS
    
        #requirements.txt
        Flask==2.2.5
        joblib==1.3.2
        numpy==1.21.6
        pandas==1.3.5
        python-dateutil==2.8.2
        requests==2.31.0
        scikit-learn==1.0.2

        #install packages
        pip install -r requirements.txt

![image](https://github.com/juliuschou/juliuschou-hellowWorldFlaskAWSElasticBeanstalkPipeline/assets/4725611/ae133c4f-1f81-4d5a-ba91-64f9997ec49d)

    
1.2.  **Create a Flask App**: 
- Create a WORKDIRDIR folder named webapp. Create a Python script, like `app.py` in webapp folder, where you import Flask and initialize a Flask web application.

1.3.  **Train scikit-learn Model**: 
- Train a new scikit-learn model and dump the model into a joblib file. Copy the joblib to webapp.

    
1.4.  **Load scikit-learn Model**: 
- Within `app.py`, load a pre-trained model. You can use joblib or pickle to load the model.
    
1.5.  **Predictive Endpoint**: 
- Create a Flask route (e.g., `/predict`) that uses the trained scikit-learn model to make predictions based on input data.
    
1.6.  **Example Endpoint**: 
- Create another Flask route (e.g., `/example`) that returns an example GET request to interact with the model.
    
1.7.  **Metadata Endpoint**: 
- Create yet another Flask route (e.g., `/metadata`) that returns metadata about the model like algorithm used, feature importance, etc.
    

# 2: Containerize the Flask Application with Docker

2.1.  **Install Docker**: If you haven't already, install Docker on your machine.
	
- **Step 1.** Update Software Repositories
		
    It's a good idea to make sure your local software repositories are up to date.
				
        sudo apt update 

- **Step 2.** Install Dependencies
	
    Install some essential packages that are necessary for Docker and its components.
    		
        sudo apt install apt-transport-https ca-certificates curl software-properties-common
    		 
		
- **Step 3.** Add Docker’s GPG Key

    Next, you can add Docker's GPG key for a secure installation.
  		
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  		 

- **Step 4.** Add Docker Repository
		
    Now, add the Docker repository to your system.

        sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
		 

- **Step 5.** Update Software Repositories Again
    
    Run the apt update command again to refresh your local database with the Docker packages.
			
        sudo apt update
		 

- **Step 6.** Install Docker
    
    Now, you can install Docker.
				
        sudo apt install docker-ce
		 

- **Step 7.** Enable and Start Docker
        
    Finally, enable and start the Docker service.
				
        sudo systemctl enable docker
        sudo systemctl start docker
    		 

- **Step 8.** Verify Installation
    
    To verify that Docker was installed correctly, you can run the following command which will download a test image and run a container from it.
		
        sudo docker run hello-world
		 
    If you see a message that says something along the lines of "Hello from Docker!", your installation has been successful.    

2.2.  **Create a `Dockerfile`**: In the root of your project, create a `Dockerfile` that starts with a base Python image and copies your project files into the container.
    
2.3.  **Build Docker Image**: Run `docker build` to create a Docker image of your application.
    
2.4.  **Run Docker Container**: Run a container from the built image and map the necessary ports.
    
2.5.  **Test the Container**: Send requests to the containerized application to make sure everything is working as expected.
    

## Code snippets for illustration:

### app.py


    from flask import Flask, request, jsonify
    
    import json
    import joblib
    from sklearn.preprocessing import StandardScaler
    import numpy as np
    
    app = Flask(__name__)
    
    def scale(payload):
        scaler = StandardScaler().fit(payload)
        return scaler.transform(payload)
    
    @app.route("/")
    def home():
        return "<h3>Sklearn Prediction Container</h3>"
    
    @app.route("/predict", methods=['POST'])
    def predict():
        """
            Input sample:
        		{
        		  "MedInc": 3.2596,
        		  "HouseAge": 33,
        		  "AveRooms": 5.017657,
        		  "AveBedrms": 1.006421,
        		  "Population": 2300,
        		  "AveOccup": 3.691814,
        		  "Latitude": 32.71,
        		  "Longitude": -117.03
        		}
    
            Output sample:
                {"prediction" : [1.9372587405453814]}
        """
        try:
            loaded_model = joblib.load("california_housing_prediction.joblib")
    
            # Since you're expecting JSON, you can use request.json directly
            data_dict = request.json
    
            values_list = list(data_dict.values())
            sample_data_point = np.array([values_list])
    
            predicted_value = loaded_model.predict(sample_data_point)
    
            # Convert the NumPy array to a Python list
            return jsonify({'prediction': predicted_value.tolist()})
    
        except Exception as e:
            return jsonify({'error': str(e)})
    
    @app.route("/metadata", methods=["GET"])
    def metadata():
        try:
            # Load the trained model from the file
            loaded_model = joblib.load("california_housing_prediction.joblib")
        except Exception as e:
            return jsonify({"error": str(e)})
    
        # Extract model metadata
        coef = loaded_model.coef_
        intercept = loaded_model.intercept_
    
        feature_names = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
    
        feature_coef_map = {}
        for feature, coef_value in zip(feature_names, coef):
            feature_coef_map[feature] = coef_value
    
        return jsonify({
            "model_coefficients": feature_coef_map,
            "model_intercept": intercept,
        })
    
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=True)

### Tran and dump a new train a new scikit-learn model - californiaHousingPricingPrediction.py
		
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    import joblib
    
    from sklearn.datasets import fetch_california_housing
    
    # Load the california Housing dataset
    california = fetch_california_housing()
    X = california.data
    y = california.target
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Save the trained model
    joblib.dump(model, "california_housing_prediction.joblib")


### `Dockerfile`


    FROM python:3.7
    
    ARG VERSION
    
    LABEL org.label-schema.version=$VERSION
    
    COPY ./california_housing_prediction.joblib /webapp/california_housing_prediction.joblib
    
    COPY ./requirements.txt /webapp/requirements.txt
    
    WORKDIR /webapp
    
    RUN pip install -r requirements.txt
    
    COPY webapp/* /webapp
    
    ENTRYPOINT ["python"]
    
    CMD ["app.py"]


### Commands to build and run Docker container

    # Build the container image
    docker build --build-arg VERSION=Auto_287f444c -t flask-predict .
    
    #Double-check that the image is now available after building
    docker images flask-predict
    
    # Run the container in the background
    docker run -p 5000:5000 -d --name flask-predict flask-predict  

# 3: Test and Deploy

3.1.  **Test the Application**: Make sure to test your Flask routes thoroughly. - callFlaskPredict.py

    import requests
    
    # Prepare the data payload
    payload = {
        "MedInc": 3.2596,
        "HouseAge": 33,
        "AveRooms": 5.017657,
        "AveBedrms": 1.006421,
        "Population": 2300,
        "AveOccup": 3.691814,
        "Latitude": 32.71,
        "Longitude": -117.03
    }
    
    # Make the POST request
    response = requests.post(
        "http://127.0.0.1:5000/predict",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    # Parse and print the response
    if response.status_code == 200:
        print("Predicted value:", response.json()['prediction'])
    else:
        print("Failed to get a prediction. Status code:", response.status_code)
    
I utilized ChatGPT to enhance this guide, as English is my second language.
    


