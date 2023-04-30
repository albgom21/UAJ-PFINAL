using P3;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using static P3.TrackerEvent;

public class FirstDoor : MonoBehaviour
{
    private bool open;
    // Start is called before the first frame update
    void Start()
    {
        open = false;
    }

    internal void OpenFirstDoor()
    {
        if (open) return;
        open = true;
        Tracker.TrackEvent(new openFirstDoorEvent());
    }
}
