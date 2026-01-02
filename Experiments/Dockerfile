FROM python:3.12

RUN pip install numpy pandas scikit-learn sympy

COPY data data

COPY NuWLS-c-IBR NuWLS-c-IBR

COPY wcnf wcnf

COPY *.py .

COPY replay_exp.sh .

CMD ["./replay_exp.sh"]