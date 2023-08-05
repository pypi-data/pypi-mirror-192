"""
APINexus
Class definition
"""
import json

import pandas
import pandas as pd
import requests
import urllib3
from pandas import json_normalize
from nexus_api.NexusRequest import NexusRequest
from nexus_api.NexusValue import NexusValue
from nexus_api.exceptions import VoidDataframeException, CorruptDataframeException, NexusAPIException
import warnings


def WarningsAndJson(func):
    """Decorator including InsecureRequestWarning and then JSON() format"""

    def f(*args, **kwargs):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        rv = func(*args, **kwargs)
        if rv.status_code == 200:
            return rv.json()
        else:
            raise NexusAPIException(rv)

    return f


def no_row_limit_decorator(fnc):
    """Decorator to remove row limit in post methods"""

    def wrapper(*args, **kwargs):
        NX = args[0]
        df_nexus = args[1]
        n = len(df_nexus)
        if n > 49999:
            iter = round(n / 49999)
            for j in range(iter):
                ini = j * 49999
                fin = (j + 1) * 49999
                if fin < n:
                    df_nexus_write = df_nexus[ini:fin]
                else:
                    df_nexus_write = df_nexus[ini:n]
                response = fnc(NX, df_nexus_write)
        else:
            response = fnc(NX, df_nexus)
        return response

    return wrapper


class APINexus:
    def __init__(self, IP_Maquina="localhost", Puerto=56000, token="", version="1.0", logger=None):
        """
        Metodo de inicialización de la clase. Aquí se define la IP y el puerto al que hemos de conectar así como el token

        Args:
            IP_Maquina (str): url de nexus
            Puerto (int): puerto de la API. 56000 de forma predeterminada
            token (str): token de la API
            version (str): 1.0 o 2.0 de momento. 1.0 by default
        """
        self.IP_Maquina = IP_Maquina
        self.Puerto = str(Puerto)
        self.token = token
        self.version = version
        self.url_NX = "http://" + IP_Maquina + ":" + str(Puerto)
        self.header = {
            "nexustoken": self.token,
            "nexusapiversion": self.version,
            "Content-Type": "application/json",
        }
        self.logger = logger
        self.log_print("Creada nueva instancia de tipo NEXUS API")

    def log_print(self, message, severity='info'):
        if self.logger is not None:
            if severity=='info':
                self.logger.info(message)
            elif severity=='error':
                self.logger.error(message)
            elif severity=='debug':
                self.logger.debug(message)
            else:
                raise ValueError('Severity not supported')
        else:
            print(message)


    def __json_normalize_check(self, response) -> pd.DataFrame:
        """
        Intenta convertir a DataFrame la respuesta en json de la API. Si no es posible, es que ha habido un fallo (la respuesta no sigue el formato establecido)
        Args:
            response: json con valor de la llamada a NexusAPI
        """
        try:
            return json_normalize(response)
        except Exception as e:
            self.log_print(f'Error de comunicación en NexusAPI. Motivo: {e}')
            raise NexusAPIException(response)

    def statusConnection(self, url_completa):
        """COD respuesta de la API"""
        resp = requests.get(url_completa, headers=self.header)
        return resp.status_code

    @WarningsAndJson
    def __getResponse(self, url):
        """GET method using Request"""
        return requests.get(url, verify=False, headers=self.header)

    @WarningsAndJson
    def __postResponse(self, url, body):
        """POST method using Request"""
        return requests.post(url, verify=False, headers=self.header, data=body)

    def callGetDocuments(self):
        """Lectura de vistas compartidas con el mismo token"""
        url_completa = self.url_NX + "/api/Documents"
        return self.__getResponse(url_completa)

    def callGetTagViews(self, uid):
        """Lectura de variables contenidas en una vista. Como parametros recibe unicamente el uid de la vista que queremos leer ya que el token , la IP y el puerto ya se han definido en la instanciacion de la clase"""
        url = self.url_NX + "/api/Documents/tagviews/" + uid
        return self.__getResponse(url)

    def callGetTagViewsRealTime(self, uid, uids_vbles):
        """Lectura de variables de una vista. Devuelve el valor en tiempo real de las variables establecidas en el array uids, contenidas en la vista uid """
        body = json.dumps(uids_vbles)
        url = self.url_NX + "/api/Documents/tagviews/" + uid + "/realtime"
        return self.__postResponse(url, body)

    def callGetDataviewHistory(self, uid, nexusRequest):
        """Lectura de valores historicos de variables"""
        body = json.dumps(
            nexusRequest, default=lambda o: o.__dict__, sort_keys=True, indent=2
        )
        url = self.url_NX + "/api/Documents/tagviews/" + uid + "/historic"
        return self.__postResponse(url, body)

    def callGetTagsWritable(self):
        """Metodo de consultas de tags escribibles"""
        url = self.url_NX + "/api/Tags/writable"
        return self.__getResponse(url)

    def callGetTags(self):
        """Método de consulta de tags de la instalación"""
        url = self.url_NX + "/api/Tags"
        return self.__getResponse(url)

    def callGetTagsRealTime(self, uids_vbles):
        """Devuelve valor RT de los tags de la instalacion definidos en un array UIDS_VBLES"""
        body = json.dumps(uids_vbles)
        url = self.url_NX + "/api/Tags/realtime"
        return self.__postResponse(url, body)

    def callGetTagsHistory(self, nexusRequest):
        """Devuelve valor historico de los tags especificados en la estructura NexusRequest"""
        body = json.dumps(nexusRequest, default=lambda o: o.__dict__, sort_keys=True, indent=2)
        url = self.url_NX + "/api/Tags/historic"
        return self.__postResponse(url, body)

    # TODO: Eliminar el header personalizado de alarmas cuando la versión de la API sea acumulativa
    @WarningsAndJson
    def callGetAlarms(self):
        """Lectura de alarmas compartidas con el mismo token"""
        header = self.header.copy()
        header['nexusapiversion'] = '2.0'
        url_completa = self.url_NX + "/api/Alarms"
        return requests.get(url_completa, verify=False, headers=header)

    @WarningsAndJson
    def callGetAlarmByuid(self, uid):
        """Lectura de alarmas compartidas con el mismo token"""
        header = self.header.copy()
        header['nexusapiversion'] = '2.0'
        url_completa = self.url_NX + "/api/Alarms/alarm/" + uid
        return requests.get(url_completa, verify=False, headers=header)

    # @WarningsAndJson -- no se necesita ya que se requiere comparar el objeto response
    def callPostAckAlarm(self, uid, status: str):
        """Lectura de alarmas compartidas con el mismo token
        status: 'ARE' or 'EXR'
        """
        if status == 'ARE' or status == 'EXR':
            header = self.header.copy()
            header['nexusapiversion'] = '2.0'
            url_completa = self.url_NX + "/api/Alarms/alarm/" + uid + "/acknowledge"
            body = "\"" + status + "\""
            return requests.post(url_completa, verify=False, headers=header, data=body)
        else:
            raise ValueError("Status must be 'ARE' or 'EXR'")

    # @WarningsAndJson
    def callPostAlarmEvent(self, uid, msg: str):
        """
        Usado para insertar mensajes en el histórico de la alarma con uid específico
        args:
            uid: uid de la alarma
        """
        header = self.header.copy()
        header['nexusapiversion'] = '2.0'
        url_completa = self.url_NX + "/api/Alarms/alarm/" + uid + "/event"
        return requests.post(url_completa, verify=False, headers=header, json={'Message': msg})

    def callPostTagInsert(self, variable_name):
        """consulta de tags con permisos de escritura"""
        url_get = self.url_NX + "/api/Tags/writable"
        variables = self.__getResponse(url_get)
        variables_names = list()
        try:
            variables_norm = self.__json_normalize_check(variables)
            variables_names = list(variables_norm.name)
        except:
            self.log_print(variables_names)

        if not variable_name in variables_names:
            self.log_print("Se procede a crear la variable con nombre "
                  + variable_name
                  + ". Se devuelve json con uid y nombre de variable creada"
                  )
            payload = '["' + variable_name + '"]'
            self.log_print(payload)
            url_post = self.url_NX + "/api/Tags/insert"
            self.log_print(url_post)
            response = self.__postResponse(url_post, payload)
            dataReceived = self.__json_normalize_check(response)
        else:
            self.log_print(
                "La variable ya existe, no se creará ninguna variable. Se devuelve el json con el uid de la variable existente"
            )
            dataReceived = variables_norm[variables_norm.name == variable_name]

        return dataReceived

    def get_rt_data_tagview(self, uid_tagview: str = None, filters=None):
        """
        Gets the real time data from Nexus.
        Args:
            NX: Nexus object
            uid_tagview: uid of the tagview. If None, it will select the first one from the token
            filters: name of the variables to filter. If None, it will select all the variables
        Returns:
            df: dataframe with the data
        """
        if uid_tagview is None:
            tagviews = self.callGetDocuments()
            tagviews = self.__json_normalize_check(tagviews)
            uid_tagview = tagviews.uid[0]
        vbles = pd.DataFrame(self.callGetTagViews(uid_tagview))['columns']
        vbles = self.__json_normalize_check(vbles)
        if filters is None:
            uids = vbles['uid'].to_list()
        else:
            filters = [filters] if isinstance(filters, str) else filters
            uids = vbles[vbles.name.isin(filters)].uid.to_list()
        # Read RT values from tagview
        data = self.__json_normalize_check(self.callGetTagViewsRealTime(uid_tagview, uids))
        diccio = dict([(i, j) for i, j in zip(vbles.uid, vbles.name)])
        data['timeStamp'] = pd.to_datetime(data['timeStamp'], unit='s')
        data['name'] = data['uid'].map(diccio)
        return data

    def callPostValueRT(self, variable_name, variable_value):
        """Escritura de variable en tiempo real.
        args:
            variable_name: nombre de la variable a escribir
            variable_value: valor de la variable a escribir
        """
        # La función comprueba primero si existe la variable en la que se quiere escribir
        url = self.url_NX + "/api/Tags/writable"
        # self.log_print(url_completa)
        variables = self.__getResponse(url)
        variables_norm = self.__json_normalize_check(variables)
        variables_names = list(variables_norm.name)

        # La función escribe en la variable
        if variable_name in variables_names:
            variable_uid = list(
                variables_norm[variables_norm.name == variable_name].uid
            )[0]
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url_completa = self.url_NX + "/api/Tags/realtime/insert"
            nexusvalue = NexusValue(variable_uid, variable_value)
            payload = (
                    "["
                    + json.dumps(
                nexusvalue, default=lambda o: o.__dict__, sort_keys=False, indent=2
            )
                    + "]"
            )
            # self.log_print(payload)
            # payload= "[{\"uid\": \"" + variable_uid + "\",\"value\": " + str(variable_value) + ",\"timeStamp\": " + str(timestamp) + "}]"

            headers = {
                "nexustoken": self.token,
                "nexusapiversion": self.version,
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url_completa, headers=headers, data=payload
            )

            if response.status_code == 200:
                dataReceived = "Escritura correcta"
            else:
                dataReceived = (
                        "Se ha intentado escribir en la variable "
                        + variable_name
                        + " con uid "
                        + variable_uid
                        + " pero la operación ha fallado"
                )
                self.log_print(response.text.encode("utf8"))
        # Si no existe, devuelve un mensaje para que el usuario cree la variable deseada (no lo hace automático para evitar creación de variables por errores tipográficos
        else:
            dataReceived = "La variable en la que se ha solicitado escribir no existe. Por favor creela mediante la función callPostTagInsert"

        return dataReceived

    def callPostValue_operate(self, variable_uid, variable_value):
        """Escritura de variable en tiempo real.
        args:
            variable_uid: nombre de la variable a escribir en el PLC
            variable_value: valor de la variable a escribir
        """

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url_completa = self.url_NX + "/api/Tags/operate"
        nexusvalue = NexusValue(variable_uid, variable_value)
        payload = (
                "["
                + json.dumps(
            nexusvalue, default=lambda o: o.__dict__, sort_keys=False, indent=2
        )
                + "]"
        )

        headers = {
            "nexustoken": self.token,
            "nexusapiversion": self.version,
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", url_completa, headers=headers, data=payload
        )

        if response.status_code == 200:
            dataReceived = "Escritura correcta"
        else:
            dataReceived = (
                    "Se ha intentado escribir en la variable "
                    + " con uid "
                    + variable_uid
                    + " pero la operación ha fallado"
            )
        self.log_print(response.text.encode("utf8"))
        # Si no existe, devuelve un mensaje para que el usuario cree la variable deseada (no lo hace automático para evitar creación de variables por errores tipográficos

        return dataReceived

    @no_row_limit_decorator
    def callPostValueHist(self, df_value_timestamp):
        """Función de escritura de variable para diferentes historicos.
        args:
            df_value_timestamp: dataframe con las variables y sus valores y timestamp
        """
        # la funcion mira cuantas variables diferentes contiene el dataframe y comprueba si todas ellas existen
        vbles = list(df_value_timestamp.name.unique())
        n = len(vbles)
        self.log_print('se intenta escribir en ' + str(n) + ' variables')
        # La función comprueba primero si existe la variable en la que se quiere escribir
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url_completa = self.url_NX + "/api/Tags/writable"
        response = requests.get(url_completa, verify=False, headers=self.header)
        variables = response.json()
        variables_pd = pandas.DataFrame(variables)
        variables_norm = self.__json_normalize_check(variables)
        diccio = dict([(i, j) for i, j in zip(variables_pd.name, variables_pd.uid)])

        variables_names = list(variables_norm.name)
        NOK = 0
        for j in vbles:
            if j not in variables_names:
                NOK = 1
                self.log_print('la variable ' + str(j) + 'no esta creada ')

        if NOK == 0:
            df2 = df_value_timestamp.copy()
            df2['uid'] = df2['name'].map(diccio)

            df2.drop(columns=["name"], inplace=True)
            if df2['timeStamp'].dtype == 'datetime64[ns]':
                warnings.warn('timeStamp in datetime format: please check that it is in UTC')
                df2['timeStamp'] = df2['timeStamp'].astype('int64') / 1e9
            self.log_print(str(df2))
            payload = pandas.DataFrame.to_json(
                df2, date_format="epoch", orient="records"
            )
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url_completa = self.url_NX + "/api/Tags/historic/insert"
            headers = {
                "nexustoken": self.token,
                "nexusapiversion": self.version,
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url_completa, headers=headers, data=payload
            )

            if response.status_code == 200:
                dataReceived = "Escritura correcta"
            else:
                dataReceived = (
                        "Se ha intentado escribir en la variable "
                        + " pero la operación ha fallado" + str(response.status_code)
                )
                self.log_print(response.text.encode("utf8"))
        # Si no existe, devuelve un mensaje para que el usuario cree la variable deseada (no lo hace automático para evitar creación de variables por errores tipográficos
        else:
            dataReceived = "La variable en la que se ha solicitado escribir no existe. Por favor creela mediante la función callPostTagInsert"
            payload = []

        return dataReceived, payload

    @no_row_limit_decorator
    def callPostValueHistmult(self, df_value_timestamp):
        """Deprecated. Use callPostValueHist instead.
        Función de escritura de variable para diferentes historicos.
        args:
            df_value_timestamp: dataframe con las variables y sus valores y timestamp
        """
        # la funcion mira cuantas variables diferentes contiene el dataframe y comprueba si todas ellas existen
        vbles = list(df_value_timestamp.name.unique())
        n = len(vbles)
        self.log_print('se intenta escribir en ' + str(n) + ' variables')
        # La función comprueba primero si existe la variable en la que se quiere escribir
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url_completa = self.url_NX + "/api/Tags/writable"
        response = requests.get(url_completa, verify=False, headers=self.header)
        variables = response.json()
        variables_pd = pandas.DataFrame(variables)
        variables_norm = self.__json_normalize_check(variables)
        diccio = dict([(i, j) for i, j in zip(variables_pd.name, variables_pd.uid)])

        variables_names = list(variables_norm.name)
        NOK = 0
        for j in vbles:
            if j not in variables_names:
                NOK = 1
                self.log_print('la variable ' + str(j) + 'no esta creada ')

        if NOK == 0:
            df2 = df_value_timestamp.copy()
            df2['uid'] = df2['name'].map(diccio)

            df2.drop(columns=["name"], inplace=True)
            if df2['timeStamp'].dtype == 'datetime64[ns]':
                warnings.warn('timeStamp in datetime format: please check that it is in UTC')
                df2['timeStamp'] = df2['timeStamp'].astype('int64') / 1e9
            self.log_print(str(df2))
            payload = pandas.DataFrame.to_json(
                df2, date_format="epoch", orient="records"
            )
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url_completa = self.url_NX + "/api/Tags/historic/insert"
            headers = {
                "nexustoken": self.token,
                "nexusapiversion": self.version,
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url_completa, headers=headers, data=payload
            )

            if response.status_code == 200:
                dataReceived = "Escritura correcta"
            else:
                dataReceived = (
                        "Se ha intentado escribir en la variable "
                        + " pero la operación ha fallado" + str(response.status_code)
                )
                self.log_print(response.text.encode("utf8"))
        # Si no existe, devuelve un mensaje para que el usuario cree la variable deseada (no lo hace automático para evitar creación de variables por errores tipográficos
        else:
            dataReceived = "La variable en la que se ha solicitado escribir no existe. Por favor creela mediante la función callPostTagInsert"
            payload = []

        return dataReceived, payload

    @no_row_limit_decorator
    def callPostValueRTmult(self, df_variable_name_value):
        """Escritura de variable en tiempo real.
        args:
            df_variable_name_value: dataframe con las variables y valores a escribir
        """
        vbles = list(df_variable_name_value.name.unique())
        n = len(vbles)
        # La función comprueba primero si existe la variable en la que se quiere escribir
        url = self.url_NX + "/api/Tags/writable"
        variables = self.__getResponse(url)
        variables_pd = pandas.DataFrame(variables)
        variables_norm = self.__json_normalize_check(variables)
        diccio = dict([(i, j) for i, j in zip(variables_pd.name, variables_pd.uid)])
        df2 = df_variable_name_value
        df2['uid'] = df2['name'].map(diccio)
        df2.drop(columns=["name"], inplace=True)
        payload = pandas.DataFrame.to_json(df2, date_format="epoch", orient="records")

        variables_names = list(variables_norm.name)
        NOK = 0
        for j in vbles:
            if j not in variables_names:
                NOK = 1
                self.log_print('la variable ' + str(j) + 'no esta creada')

        if NOK == 0:
            # La función escribe en la variable
            self.log_print('se actualiza el valor RT de ' + str(n) + ' vbles')
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url_completa = self.url_NX + "/api/Tags/realtime/insert"
            headers = {
                "nexustoken": self.token,
                "nexusapiversion": self.version,
                "Content-Type": "application/json",
            }
            response = requests.request("POST", url_completa, headers=headers, data=payload)
            if response.status_code == 200:
                dataReceived = "Escritura correcta"
            else:
                dataReceived = (
                        "Se ha intentado escribir en la variable "
                        + " pero la operación ha fallado" + str(response.status_code)
                )
                self.log_print(response.text.encode("utf8"))

        return dataReceived

    def filter_installation(self, Datefrom, Dateto, columnas, filter_txt=None, uids=None, resolucion=3,
                            fuente=0) -> pd.DataFrame:
        """
        la funcion recibe como parametros la fecha ini, fecha fin, un df con los uid y
        los nombres de las variables de la instalación y el filtro de texto aplicar

        Args:
            Datefrom (datetime)
            Dateto (datetime)
            columnas (dataframe)
            uids: (optional) (list): lista de los uids de las variables deseadas. No puede usarse con filter_txt
            filter_txt (optional: list or str): lista de nombres de las variables deseadas. No puede usarse con uids
            resolucion (int): de 0 a 10 [ RES_30_SEC, RES_1_MIN, RES_15_MIN, RES_1_HOUR, RES_1_DAY, RES_1_MONTH, RES_1_YEAR, RES_5_MIN, RES_200_MIL, RES_500_MIL, RES_1_SEC ]
            fuente (int): [0 -->RAW, 1 -->STATS_PER_HOUR, 2 -->STATS_PER_DAY, 3 -->STATS_PER_MONTH, 4 -->TRANSIENT]
        Returns:
            filtered_hist (dataframe)
        """
        # Check parameters
        if uids is not None and filter_txt is not None:
            raise ValueError('Error en uids y filter_txt. No pueden usarse ambos parámetros de búsqueda')
        if uids is None:
            uids = []
            if isinstance(filter_txt, list):
                for filter in filter_txt:
                    uids_loop = list(columnas[columnas['name'].str.contains(filter, case=False)].uid)
                    uids.extend(uids_loop)
            else:
                if filter_txt:
                    uids = list(columnas[columnas['name'].str.contains(filter_txt, case=False)].uid)
            if not uids:
                self.log_print('Los filtros proporcionados no encuentran ninguna variable. Se devolverá toda la instalación')
                uids = list(columnas.uid)
        # Remove duplicate UIDS
        uids = list(set(uids))
        fecha_ini = Datefrom
        fecha_fin = Dateto
        nexusRequest = NexusRequest(uids, fecha_ini, fecha_fin, fuente, resolucion)
        filtered_hist = self.callGetTagsHistory(nexusRequest)
        filtered_hist = self.__json_normalize_check(filtered_hist)
        # Check that there is no error in the dataframe
        self.__check_response_error_df(filtered_hist)
        filtered_hist.timeStamp = pandas.to_datetime(filtered_hist.timeStamp, unit='s')
        diccio = dict([(i, j) for i, j in zip(columnas.uid, columnas.name)])
        filtered_hist['name'] = filtered_hist['uid'].map(diccio)
        return filtered_hist

    def filter_tagview(self, Datefrom, Dateto, columnas, uid_vista, filter_txt=None, uids=None, resolucion=3,
                       fuente=0) -> pd.DataFrame:
        """
        La funcion recibe como parametros la fecha ini, fecha fin, un df con los uid y
        los nombres de las variables de la instalación y el filtro de texto aplicar [pueden ser varios]
        Args:
            Datefrom (datetime)
            Dateto (datetime)
            columnas (dataframe)
            uid_vista: uid de la vista en la que se busca
            uids: (optional) (list): lista de los uids de las variables deseadas. No puede usarse con filter_txt
            filter_txt (optional: list or str): lista de nombres de las variables deseadas. No puede usarse con uids
            resolucion (int): de 0 a 10 [ RES_30_SEC, RES_1_MIN, RES_15_MIN, RES_1_HOUR, RES_1_DAY, RES_1_MONTH, RES_1_YEAR, RES_5_MIN, RES_200_MIL, RES_500_MIL, RES_1_SEC ]
            fuente (int): [0 -->RAW, 1 -->STATS_PER_HOUR, 2 -->STATS_PER_DAY, 3 -->STATS_PER_MONTH, 4 -->TRANSIENT]
        Returns:
            filtered_hist (dataframe)
        """
        # Check parameters
        if uids is not None and filter_txt is not None:
            raise ValueError('Error en uids y filter_txt. No pueden usarse ambos parámetros de búsqueda')
        if uids is None:
            uids = []
            if isinstance(filter_txt, list):
                for filter in filter_txt:
                    uids_loop = list(columnas[columnas['name'].str.contains(filter, case=False)].uid)
                    uids.extend(uids_loop)
            else:
                if filter_txt:
                    uids = list(columnas[columnas['name'].str.contains(filter_txt, case=False)].uid)
            if not uids:
                self.log_print('Los filtros proporcionados no encuentran ninguna variable. Se devolverá toda la instalación')
                uids = list(columnas.uid)
        # Remove duplicate UIDS
        uids = list(set(uids))
        fecha_ini = Datefrom
        fecha_fin = Dateto
        # fuente: [0 -->RAW, 1 -->STATS_PER_HOUR, 2 -->STATS_PER_DAY, 3 -->STATS_PER_MONTH, 4 -->TRANSIENT]
        # resolucion: de 0 a 10 [ RES_30_SEC, RES_1_MIN, RES_15_MIN, RES_1_HOUR, RES_1_DAY, RES_1_MONTH, RES_1_YEAR,
        # RES_5_MIN, RES_200_MIL, RES_500_MIL, RES_1_SEC ]
        nexusRequest = NexusRequest(uids, fecha_ini, fecha_fin, fuente, resolucion)
        filtered_hist = self.callGetDataviewHistory(uid_vista, nexusRequest)
        filtered_hist = self.__json_normalize_check(filtered_hist)
        # Check dataframe for errors
        self.__check_response_error_df(filtered_hist)
        filtered_hist.timeStamp = pandas.to_datetime(filtered_hist.timeStamp, unit='s')
        diccio = dict([(i, j) for i, j in zip(columnas.uid, columnas.name)])
        filtered_hist['name'] = filtered_hist['uid'].map(diccio)
        return filtered_hist

    def get_alarms_uids_by_names(self, names):
        alarms = self.__json_normalize_check(self.callGetAlarms())
        names = [names] if isinstance(names, str) else names
        uids = alarms['uid'][alarms['name'].isin(names)]
        return uids

    def get_alarms_uids_by_groups(self, groups):
        alarms = self.__json_normalize_check(self.callGetAlarms())
        groups = [groups] if isinstance(groups, str) else groups
        uids = []
        for group in groups:
            uids.extend(alarms['uid'][alarms['group'].str.contains(group, case=False)].to_list())
        return uids

    def __check_response_error_df(self, filtered_hist: pd.DataFrame) -> None:
        """
        Checks the received dataframe from API request and raises an error if not valid
        """
        # Check that there is no error in the dataframe
        if 'StatusCode' in filtered_hist.keys():
            message = filtered_hist['Message']
            code = filtered_hist['StatusCode']
            ex_message = f'Status Code: {code}: {message}'
            raise ValueError(ex_message)
        # Check that dataframe is not empty
        elif filtered_hist.empty:
            raise VoidDataframeException
        # Check content
        elif not {'timeStamp', 'uid', 'value'}.issubset(filtered_hist.columns):
            raise CorruptDataframeException(filtered_hist)
        else:
            pass
