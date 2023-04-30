using System;
using System.Collections;
using System.Security.Cryptography;
using System.Text;
using UnityEngine;

namespace P3
{
    public class Tracker
    {
        public static Tracker instance = null;
        private static IPersistance persistenceObject = null;  // Persistencia
        private static string sessionID;                       // ID único de la sesión  
        private static bool activeTracker;                     // Bool para saber si está activo el Tracker
        private static float timeToFlushEvents;                // Tiempo entre cada persistencia

        // Constructor privado para evitar la creación de instancias fuera de la clase
        private Tracker() { }

        // Método para obtener la instancia única del Singleton
        public static Tracker Instance
        {
            get
            {
                if (instance == null)
                    instance = new Tracker();

                return instance;
            }
        }

        // Método para inicializar la instancia única del Singleton
        public static bool Init()
        {
            if (instance == null)
                instance = new Tracker();

            if (instance == null)
                return false;

            //------Estudiar si meter esto en otro método por si falla para que se inicie correctamente el Tracker------

            // Generar un ID para la sesión único
            sessionID = GenerateUniqueId(DateTimeOffset.Now.ToUnixTimeSeconds().ToString());

            // El serializer puede ser de otro tipo si tenemos más, refactorizar en ese caso
            // RUTA C:\Users\(NOMBRE DEL USUARIO EN WINDOWS)\AppData\LocalLow\DefaultCompany\Pulse_P1
            persistenceObject = new FilePersistance(Application.persistentDataPath + "/Persistencia"+ sessionID + ".json", new JSONSerializer());

            // Trackear el evento de inicio de la sesión
            TrackEvent(new iniSessionEvent());

            // Marcar como activo el Tracker
            activeTracker = true;

            timeToFlushEvents = 5f;
            return true;
        }

        // Método para finalizar la instancia única del Singleton
        public void End()
        {
            // Marcar como desactivado el Tracker
            activeTracker = false;

            // Trackear el evento de final de sesión
            TrackEvent(new endSessionEvent());

            // Guardar los eventos que estuvieran en cola
            persistenceObject.Flush();

            instance = null;
        }

        // Persistir un evento
        public static void TrackEvent(TrackerEvent e)
        {
            persistenceObject.Send(e);
        }

        // Mientras esté activo el Tracker cada X segundos llamar al módulo de persistencia
        public static IEnumerator FlushEvents()
        {
            while (activeTracker)
            {
                yield return new WaitForSeconds(timeToFlushEvents);
                persistenceObject.Flush();
            }
        }

        public static string GenerateUniqueId(string obj)
        {
            // Convierte la cadena en un arreglo de bytes utilizando UTF-8
            byte[] bytes = Encoding.UTF8.GetBytes(obj);

            // Calcula el valor hash SHA256
            SHA256 sha256 = SHA256.Create();
            byte[] hash = sha256.ComputeHash(bytes);

            // Convierte el valor hash en una cadena de texto hexadecimal
            StringBuilder sb = new StringBuilder();
            foreach (byte b in hash)
                sb.Append(b.ToString("x2"));

            // Devuelve la cadena resultante como identificador único
            return sb.ToString();
        }

        // Obtener la fecha y hora actual y convertir a un timestamp de tiempo POSIX
        public long GetTimeStamp()
        {
            return DateTimeOffset.Now.ToUnixTimeSeconds();
        }

        // Devolver el ID único de la sesión
        public string GetSessionId()
        {
            return sessionID;
        }
    }
}