# AutoPen -- Backend Service

## Installation

- Requires
    - python 3.11.5 or earlier
    - mongodb cloud service
    - docker

```
pip install openai django djongo pymongo pytz django-cors-headers 
```

- Add current IP to cloud mongodb allow list.
- Modify config.ini and setting.py by your cloud service url and cluster name.
- enter Backend directory.

```
python manage.py runserver 0.0.0.0: 8000
```

## use nginx to reverse proxy for the frontend to connect
In the OPtion section, nginx needs to hadle CROS issue
```
# Respond to preflight requests
            add_header 'Access-Control-Allow-Origin' 'http://localhost:3001';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization';
            add_header 'Access-Control-Max-Age' 3600;  # Cache preflight response
            return 204;
```


- There's a third-party service, which is a documentation service that helps developers communicate with each other.

```docker
docker run -d --name showdoc -p 4999:80 -v /showdoc_data/html:/var/www/html/ star7th/showdoc
```

## Example

we already deployed a complete service on a cloud vm to show our project implementation. You can go to the address below
to browse.

- AutoPen

```
http://http://40.76.249.160:80/
```

- Documentation Service

```
http://http://40.76.249.160:8001/
```
