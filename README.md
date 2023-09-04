# UtiAIzer

## Demo



https://github.com/tamtam-fitness/UtiAIzer/assets/62091034/845d4a7d-53ac-4fca-815d-4652f04b622a



## Prerequisites

- Tool to run Docker like Docker Desktop
  - I highly recommend to use [OrbStack](https://github.com/orbstack/orbstack)

## Apply template to your project
```
git clone https://github.com/tamtam-fitness/python-template-based-on-docker.git <new-project>

cd <new-project>

rm -rf .git
```

## Run Container

To start development, you are supposed to run the following command:
```bash 
make setup   
```

## Development Commands

### Enter into container
```bash
make enter_container
```

### Lint

```bash 
make lint
```
### Format

```bash 
make format
```

### Test

If you want to run all tests, you can run the following command:
```bash 
make test
```

If you want to run the specific test, you can run the following command:
```bash
make enter_container

poetry shell

poe test tests/{file or directory you want to test}
```
