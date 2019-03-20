# Planon LDAP Sync

1. [Getting Started](#getting-started)
2. [SOAP API Setup](#soap-api-setup)

## Getting Started

### Requirements

* Python 3.X+

## SOAP API Setup

1. Login to Planon, click **Tools** --> **Web services**
    1. Click **Add** and fill in the required information

    ![Web Services](./images/example-web-services.png)

2. Search for and add the **Account** and **AccountGroup** business objects

    ![Web Services](./images/example-web-services-bos.png)

3. Click **Link field definitions** and add any required definitions, for this example we've added all fields

    ![Web Services](./images/example-web-services-bos-fields.png)

4. Click **Compile web service**, download the generated .jar file

    ![Web Services](./images/example-web-services-compile.png)

5. Login to the Axis2 administration console ```https:/<instance name>.planoncloud.com/nyx/```

    ![Apache Axis2](./images/example-axis2.png)

6. **Browse** to the .jar file and select it, click **Upload**

    >NOTE: If you have an existing web service you may need to delete it, otherwise duplicate methods will be created and errors will be thrown

    ```bash
    # Simple curl example to delete WebDAV files
    curl --user $PLANONWEBDAVUSER:$PLANONWEBDAVPWD https://<instance name>.planoncloud.com/webservices/
    ```

    ![Apache Axis2 Upload](./images/example-axis2-upload.png)

7. Verify the SOAP API methods are shown under **Services**

    ![Apache Axis2 Services](./images/example-axis2-services.png)