using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace P3
{
    // Clase que representa un evento de nuestro Tracker
    public class TrackerEvent
    {
        public enum EventType      // Tipos de eventos
        {
            INI_SESSION,           // Inicio de la sesión
            END_SESSION,           // Final de la sesión
            ENTER_ROOM,            // Entrada en una sala
            EXIT_ROOM,             // Salida en una sala
            INI_LVL,               // Inicio del nivel
            END_LVL,               // Final del nivel
            PRESS_BUTTON,          // Pulsación de botón del láser
            OPEN_FIRST_DOOR,       // Apertura primera puerta
            POS_PLAYER_ATTACK,     // Posición del jugador cuando se ataque
            POS_PLAYER_INTERACT,   // Posición del jugador cuando interactúa
            CHANGE_WEAPON,         // Cambio de arma
            POS_PLAYER_KILL,        // Posición del jugador cuando elimina a un enemigo
            POS_PLAYER_DEAD,        // Posición del jugador cuando muere
            POS_ENEMY_DEAD,         //Posición del enemigo cuando muere
            POS_ENEMY_KILL,         //Posición del enemigo cuando elimina al jugador
            AIMING,                 //Momento en el que el jugador comienza a apuntar
            NOT_AIMING              //Momento en el que el jugador deja de apuntar
        }
        public enum RoomID         // Nombres de salas ---------METER MAS TIPOS DE ROOMS---------------
        {
            ROOM_0,
            ROOM_1,
            ROOM_2,
            ROOM_3,
            ROOM_4,
            ROOM_5,
            ROOM_6,
            ROOM_7,
            ROOM_8,
            ROOM_9,
            ROOM_10,
            ROOM_11,
            ROOM_12,
            ROOM_13,
            ROOM_14,
            ROOM_15,
            ROOM_16,
            ROOM_17,
            ROOM_18,
            ROOM_19,
            ROOM_20,
            ROOM_21,
            ROOM_22,
            ROOM_23,
            ROOM_24,
            ROOM_25,
            ROOM_26,
            ROOM_27,
            ROOM_28,
            ROOM_29,
            HALL_0_1_3,
            HALL_1_2,
            HALL_2_3,
            HALL_3_4_18,
            HALL_4_5,
            HALL_5_6,
            HALL_6_7,
            HALL_7_8,
            HALL_8_9,
            HALL_9_10,
            HALL_7_11,
            HALL_9_11,
            HALL_11_12,
            HALL_5_13,
            HALL_13_14,
            HALL_14_15,
            HALL_14_16,
            HALL_16_17,
            HALL_18_19,
            HALL_14_22,
            HALL_19_20_21,
            HALL_21_22_23_24,
            HALL_24_25,
            HALL_24_26,
            HALL_26_27,
            HALL_26_28,
            HALL_26_29,
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