
Certainly! The task involves several steps, each requiring some technical skills in areas such as Docker, Flask web framework, and machine learning using scikit-learn. Here is a breakdown of the task:

# 1: Create a Flask Application with scikit-learn Model

1.1.  **Initialize a New Python Project**: 

- Create a new folder and initialize it as a Python project. Create a `requirements.txt` to list the Python packages you'll need (Flask, scikit-learn, etc.).

![image](https://github.com/juliuschou/juliuschou-hellowWorldFlaskAWSElasticBeanstalkPipeline/assets/4725611/a98c7156-77b5-4813-abfd-36e6f20d0c8a)
    
1.2.  **Create a Flask App**: 
- Create a Python script, like `app.py`, where you import Flask and initialize a Flask web application.
    
1.3.  **Train/Load scikit-learn Model**: 
- Within `app.py`, either train a new scikit-learn model or load a pre-trained model. You can use joblib or pickle to load a pre-trained model.
    
1.4.  **Predictive Endpoint**: 
- Create a Flask route (e.g., `/predict`) that uses the trained scikit-learn model to make predictions based on input data.
    
1.5.  **Example Endpoint**: 
- Create another Flask route (e.g., `/example`) that returns an example GET request to interact with the model.
    
1.6.  **Metadata Endpoint**: 
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
    
    import pandas as pd
    
    from sklearn.externals import joblib
    from sklearn.preprocessing import StandardScaler
    
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
            "CHAS":{"0": 0}, "RM":{"0": 6.575},
            "TAX":{"0": 296 }, "PTRATIO":{"0": 15.3 },
            "b":{"0": 396.9 }, "LSTAT":{"0": 4.98 }
        }
        
        Output sample:
            {"prediction" : [20.35373177134412]}
        """
        clf = joblib.load("boston_housing_prediction.joblib")
        inference_payload = pd.DataFrame(request.json)
        scaled_payload = scale(inference_payload)
        predicttion = list(clf.predict(scaled_payload))
        return  jsonify({'prediction': predicttion})
    
    @app.route('/example', methods=['GET'])
    def example():
        return jsonify({'example': 'GET /predict'})
    
    @app.route('/metadata', methods=['GET'])
    def metadata():
        return jsonify({'algorithm': 'Random Forest', 'features': ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']})
    
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=True)

### tran and dump a new train a new scikit-learn model
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    import joblib
    
    from sklearn.datasets import fetch_california_housing
    
    # Load the Boston Housing dataset
    boston = fetch_california_housing()
    X = boston.data
    y = boston.target
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Save the trained model
    joblib.dump(model, "boston_housing_prediction.joblib")


### `Dockerfile`


    FROM python:3.8
    COPY . /app
    WORKDIR /app
    RUN pip install -r requirements.txt
    CMD ["python", "app.py"]


### Commands to build and run Docker container


    docker build -t my_flask_app .
    docker run -p 5000:5000 my_flask_app
 

# 3: Test and Deploy

3.1.  **Test the Application**: Make sure to test your Flask routes thoroughly.
    
3.2.  **Deploy the Container**: Optionally, you can deploy the Docker container to a cloud service for more extensive testing or production usage.
    

That should cover most of the steps involved in fulfilling your task.
