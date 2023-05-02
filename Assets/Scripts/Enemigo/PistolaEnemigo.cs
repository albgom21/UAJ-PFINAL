using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PistolaEnemigo : MonoBehaviour
{
    [SerializeField]
    private Transform pistola = null;
    [SerializeField]
    private GameObject bala = null;
    private AudioSource fire;
    private void Start()
    {
        fire = pistola.GetComponent<AudioSource>();
    }

    public void Shoot()
    {
        GameObject balaInst = Instantiate(bala, pistola.position, Quaternion.Euler(transform.localEulerAngles));
        balaInst.GetComponent<Bullet>().SetBounce(0);
        balaInst.GetComponent<Bullet>()._Traker_SetPistola(this);
        fire.Play();
    }
}
