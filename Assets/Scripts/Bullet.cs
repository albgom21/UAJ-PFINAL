﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using P3;
using System.Numerics;

public class Bullet : MonoBehaviour
{
    private int bounces_ = 1;
    private PistolaEnemigo _tracker_pistola; //Pistola que ha disparado la bala. Su posición es la del enemigo por lo que sirve para el evento enemyKill

    void Start()
    {
        GetComponent<Rigidbody2D>().AddForce(transform.up * 10, ForceMode2D.Impulse);
        Invoke("Destroy", 5f);
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.tag == "Enemy")
        {
            Transform playerTr = GameManager.gmInstance_.GetPlayerTransform();
            Tracker.TrackEvent(new playerKillEvent(playerTr.position.x, playerTr.position.y, playerKillEvent.Weapon.PISTOL));
            collision.gameObject.GetComponent<Enemigo>().Death();
            Destroy(gameObject);
        }
        else if (collision.gameObject.tag == "Player" )
        {
            Tracker.TrackEvent(new enemyKillEvent(_tracker_pistola.transform.position.x, _tracker_pistola.transform.position.y));
            
            collision.gameObject.GetComponent<PlayerController>().Die();

            Destroy(gameObject);
        }
        if (bounces_ == 0) Destroy(gameObject);

        bounces_--;
    }

    public void SetBounce(int bounces)
    {
        bounces_ = bounces;
    }

    public void _Traker_SetPistola(PistolaEnemigo pistola)
    {
        _tracker_pistola = pistola;
    }
}
