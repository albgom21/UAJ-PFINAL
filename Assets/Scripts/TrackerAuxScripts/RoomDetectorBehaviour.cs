using P3;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RoomDetectorBehaviour : MonoBehaviour
{
    [SerializeField] private TrackerEvent.RoomID roomId;

    private bool playerInRoom;
    // Start is called before the first frame update
    void Start()
    {
        playerInRoom = false;
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        PlayerController pc = collision.GetComponent<PlayerController>();
        if (pc != null)
        {
            Tracker.TrackEvent(new enterRoomEvent(roomId));
        }
    }
    private void OnTriggerExit2D(Collider2D collision)
    {
        PlayerController pc = collision.GetComponent<PlayerController>();
        if (pc != null)
        {
            Tracker.TrackEvent(new exitRoomEvent(roomId));
        }
    }
}
