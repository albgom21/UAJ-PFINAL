using System;
using System.Collections.Generic;
using System.IO;

namespace P3
{
    public class FilePersistance : IPersistance
    {
        string path;
        ISerializer serializer;
        Queue<TrackerEvent> events;

        public FilePersistance(string path_, ISerializer serializer_)
        {
            path = path_;
            serializer = serializer_;
            events = new Queue<TrackerEvent>();
        }

        // Enviar a la cola de eventos un evento
        public override void Send(TrackerEvent te)
        {
            events.Enqueue(te);
        }

        // Copiar en disco la serialización de los eventos en cola
        public override void Flush()
        {
            TrackerEvent te;
            string eventSerialized = "";
            while (events.Count > 0)
            {
                te = events.Dequeue();                          // Obtener y quitar evento de la cola
                eventSerialized = serializer.Serialize(te);     // Serializar el evento
                try
                {
                    StreamWriter writer = new StreamWriter(path, true);  // Escribir en la ruta el evento
                    writer.WriteLine(eventSerialized);
                    writer.Close();
                }
                catch (Exception except)
                {
                    UnityEngine.Debug.LogError(except.Message);
                }
            }
        }
    }
}