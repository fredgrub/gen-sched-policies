Source material of the paper: Obtaining Dynamic Scheduling Policies with Simulation and Machine Learning.

We provide the source code implementation of all of the strategies proposed in the paper as well as the source code of the simulation experiments used to evaluate our approach so the reader can (i) generate their own distribution score(r,n,s), (ii) reproduce the nonlinear regression to obtain the scheduling policies presented in the paper or generate their own scheduling policies with their own generated distribution, and (iii) reproduce the dynamic scheduling experiments results presented in the paper.

# Usage
The entire environment is configured to run through Docker. To use it build the image
```
docker build -t sched-policies .
```

After building the image, run the container as follows (make sure you run the command in the root of the repository)
```
docker run -d -it --name sched --mount type=bind,source="$(pwd)",target=/usr/src/dev/ sched-policies:latest
```

The command above run the container in detach mode (in background, `-d`); it also connects the current folder (repository root) to the `/usr/src/dev` directory - via `--mount` flag - allowing changes made to the container to also modify files on the host.

Access to the container can be done through
```
docker exec -it sched /bin/bash
```
