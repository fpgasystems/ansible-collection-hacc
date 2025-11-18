FROM ubuntu:22.04

# --- Build arguments (can be overridden when building) ---
ARG ZIP_FILE=linux__flexm_v11.17.2.0.zip
ARG INSTALL_DIR=/opt/flexlm

# --- Install dependencies ---
RUN apt-get update && \
    apt-get install -y software-properties-common unzip lsb-core && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y unzip && \
    rm -rf /var/lib/apt/lists/*

# --- Create required directories ---
RUN mkdir -p /licenses ${INSTALL_DIR} /usr/tmp/.flexlm
WORKDIR /opt

# --- Copy ZIP into container ---
COPY ./${ZIP_FILE} .

# --- Unzip and normalize install path ---
RUN unzip ${ZIP_FILE} -d ${INSTALL_DIR} && \
    rm ${ZIP_FILE}

# --- The flexm zip contains multiple levels of dir. This removes those ---
RUN inner_dir=$(ls ${INSTALL_DIR}) && \
    mv ${INSTALL_DIR}/"$inner_dir"/"$inner_dir"/* ${INSTALL_DIR} && \
    rmdir ${INSTALL_DIR}/"$inner_dir"/"$inner_dir" && \
    rmdir ${INSTALL_DIR}/"$inner_dir" && echo "$innder_dir" > ${INSTALL_DIR}/VERSION

# --- Fix permissions ---
RUN chmod -R a+x ${INSTALL_DIR}/lnx64.o

# --- Update PATH so lmgrd can be run directly ---
ENV PATH="${INSTALL_DIR}/lnx64.o:${PATH}"

# --- Setup non-root user ---
RUN groupadd -r lmadmin && \
useradd -r -g lmadmin lmadmin

WORKDIR ${INSTALL_DIR}

EXPOSE 2100

# --- Use non-root user ---
USER lmadmin

ENTRYPOINT ["lmgrd", "-z", "-c", "/licenses"]
