using P3;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Daga : MonoBehaviour
{
    private AudioSource source;
    private Animator animator;
    private void Start()
    {
        source = GetComponent<AudioSource>();
        animator = GetComponentInParent<Animator>();
    }
    public void Attack()
    {
        if (enabled)
        {
            source.Play();
            animator.SetTrigger("Ataque");
        }
    }
    private void OnTriggerEnter2D(Collider2D collision)
    {
        Enemigo e = collision.gameObject.GetComponent<Enemigo>();
        if (e)
        {
            Transform playerTr = GameManager.gmInstance_.GetPlayerTransform();
            Tracker.TrackEvent(new playerKillEvent(playerTr.position.x, playerTr.position.y, playerKillEvent.Weapon.KNIFE));
            e.Death();
        }
    }
}