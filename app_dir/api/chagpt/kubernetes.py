apiVersion: v1
kind: ConfigMap
metadata:
  name: django-config
data:
  settings.py: |-
    DEBUG = True
    SECRET_KEY = 'your-secret-key'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mydatabase',
            'USER': 'mydatabaseuser',
            'PASSWORD': 'mypassword',
            'HOST': 'postgres',
            'PORT': '5432',
        }
    }

'''

apiVersion: apps/v1
kind: Deployment
metadata:
  name: django-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: django
  template:
    metadata:
      labels:
        app: django
    spec:
      containers:
      - name: django
        image: my-django-image
        env:
          - name: DJANGO_SETTINGS_MODULE
            value: myapp.settings
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: config-volume
          mountPath: /app/myapp/settings.py
          subPath: settings.py
      volumes:
      - name: config-volume
        configMap:
          name: django-config

'''

# kubectl apply -f configmap.yaml
# kubectl apply -f deployment.yaml



