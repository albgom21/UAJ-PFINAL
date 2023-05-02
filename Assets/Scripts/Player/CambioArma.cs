using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using P3;

public class CambioArma : MonoBehaviour
{
    [SerializeField]
    private Daga daga = null;
    [SerializeField]
    private Pistola pistola = null;
    private Animator animator;
    private bool _tracker_dagaEquipada;
    void Start()
    {
        animator = GetComponent<Animator>();
        pistola.enabled = false;
        GameManager.gmInstance_.SetWeapon(daga.enabled);
        _tracker_dagaEquipada = true;
    }

    void Update()
    {
        if (Input.GetButtonDown("WeaponChange") && !GameManager.gmInstance_.IsGamePaused())
        {
            animator.SetTrigger("Cambio arma");
            daga.gameObject.SetActive(!daga.gameObject.activeSelf);
            daga.enabled = !daga.enabled;
            pistola.enabled = !pistola.enabled;
            _tracker_dagaEquipada = !_tracker_dagaEquipada;
            _Tracker_ChangeWeaponEvent();
            GameManager.gmInstance_.SetWeapon(daga.enabled);
        }
    }

    public bool _Tracker_GetWeapon() { return _tracker_dagaEquipada; }

    private void _Tracker_ChangeWeaponEvent()
    {
        changeWeaponEvent.Weapon weapon;
        if (_tracker_dagaEquipada) weapon = changeWeaponEvent.Weapon.KNIFE;
        else weapon = changeWeaponEvent.Weapon.PISTOL;

        Tracker.TrackEvent(new changeWeaponEvent(GameManager.gmInstance_._Tracker_GetAmmo(), weapon));
    }
}
