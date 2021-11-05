ARG base
FROM ${base}

COPY . /code
ENTRYPOINT ["/bin/bash"]
CMD ["/code/entrypoint.sh"]
