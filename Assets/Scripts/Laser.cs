using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Laser : MonoBehaviour
{
    [SerializeField]
    private string layer_ = "";
    [SerializeField]
    private bool intermitencia = false;
    [SerializeField]
    private float ratio = 2f;
    private SpriteRenderer laserRenderer;
    private BoxCollider2D coll;
    [SerializeField]
    private AudioSource laser;
    [SerializeField]
    private AudioSource laserEarly;
    [SerializeField]
    private LineRenderer laserE;

    void Start()
    {
        laserRenderer = GetComponent<SpriteRenderer>();
        coll = GetComponent<BoxCollider2D>();
        gameObject.layer = LayerMask.NameToLayer(layer_);
        if (intermitencia) StartCoroutine(LaserIntermitente());
        else laser.Play();
    }

    public bool GetIntermitencia()
    {
        return intermitencia;
    }
    public void SetIntermitencia(bool inter)
    {
        intermitencia = inter;
    }

    IEnumerator LaserIntermitente()
    {
        laserEarly.Play();
        laserE.enabled = true;
        yield return new WaitForSeconds(ratio);
        laserEarly.Stop();
        laserE.enabled = false;
        coll.enabled = true;
        laserRenderer.enabled = true;
        laser.Play();
        yield return new WaitForSeconds(ratio);
        coll.enabled = false;
        laserRenderer.enabled = false;
        laser.Stop();
        yield return new WaitForSeconds(ratio);
        StartCoroutine(LaserIntermitente());
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        PlayerController detectorJugador = collision.GetComponent<PlayerController>();
        if (detectorJugador)
        {
            laser.Stop();
            detectorJugador._Tracker_SetDeathType();
            detectorJugador.Die();
        }    
    }
}
