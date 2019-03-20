# Planon LDAP Sync

1. [Getting Started](#getting-started)
2. [SOAP API Setup](#soap-api-setup)

## Getting Started

### Requirements

* Python 3.X+

## SOAP API Setup

![Web Services](./images/example-web-services.png)

![Web Services](./images/example-web-services-bos.png)

![Web Services](./images/example-web-services-bos-fields.png)

![Web Services](./images/example-web-services-compile.png)

Login to the Axis2 administration console ```https:/<instance name>.planoncloud.com/nyx/axis2-admin/welcome```

![Apache Axis2](./images/example-axis2.png)

Clear out webservices being replaced

```bash
curl --user $PLANONWEBDAVUSER:$PLANONWEBDAVPWD https://<instance name>.planoncloud.com/webservices/
```

![Apache Axis2 Upload](./images/example-axis2-upload.png)

![Apache Axis2 Services](./images/example-axis2-services.png)