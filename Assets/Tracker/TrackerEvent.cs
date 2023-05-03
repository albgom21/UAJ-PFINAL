using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace P3
{
    // Clase que representa un evento de nuestro Tracker
    public class TrackerEvent
    {
        public enum EventType       // Tipos de eventos
        {
            INI_SESSION,            // Inicio de la sesión
            END_SESSION,            // Final de la sesión
            INI_LVL,                // Inicio del nivel
            END_LVL,                // Final del nivel
            CHANGE_WEAPON,          // Cambio de arma
            POS_PLAYER_ATTACK,      // Posición del jugador cuando se ataque
            POS_PLAYER_KILL,        // Posición del jugador cuando elimina a un enemigo
            POS_PLAYER_DEAD,        // Posición del jugador cuando muere
            POS_ENEMY_DEAD,         // Posición del enemigo cuando muere
            POS_ENEMY_KILL,         // Posición del enemigo cuando elimina al jugador
            PRESS_BUTTON,           // Pulsación de botón del láser
            AIMING,                 // Momento en el que el jugador comienza a apuntar
            NOT_AIMING              // Momento en el que el jugador deja de apuntar
        }
        // Atributos mínimos que tienen todos los eventos

        public EventType tipo;  // Tipo de evento

        public long timestamp;  // Marca de tiempo en POSIX


        // Permitir que los enumerados se persistan con su nombre en lugar de su valor entero
        static JsonSerializerSettings settings = new JsonSerializerSettings
        {
            Converters = new List<JsonConverter> { new StringEnumConverter() }
        };

        // Crear evento
        public TrackerEvent(EventType t)
        {
            timestamp = Tracker.Instance.GetTimeStamp();
            tipo = t;
        }

        // Serializar a JSON
        public string ToJSON()
        {
            return JsonConvert.SerializeObject(this, settings);
        }
    }
}