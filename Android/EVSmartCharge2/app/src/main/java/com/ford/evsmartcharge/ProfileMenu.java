package com.ford.evsmartcharge;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.preference.EditTextPreference;
import android.support.v7.preference.ListPreference;
import android.support.v7.preference.Preference;
import android.support.v7.preference.PreferenceGroup;
import android.support.v7.preference.PreferenceFragmentCompat;

public class ProfileMenu extends PreferenceFragmentCompat implements SharedPreferences.OnSharedPreferenceChangeListener {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getPreferenceScreen().getSharedPreferences().registerOnSharedPreferenceChangeListener(this);

    }

    @Override
    public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
        // Load the preferences from an XML resource
        setPreferencesFromResource(R.xml.pref_profile, rootKey);
    }

    @Override
    public void onResume() {
        super.onResume();
        for(int i = 0; i < getPreferenceScreen().getPreferenceCount(); i++) {
            Preference preference = getPreferenceScreen().getPreference(i);

            if(preference instanceof PreferenceGroup) {
                PreferenceGroup preferenceGroup = (PreferenceGroup) preference;

                for(int j = 0; j < preferenceGroup.getPreferenceCount(); j++) {
                    Preference singlePref = preferenceGroup.getPreference(j);
                    updatePreference(singlePref, singlePref.getKey());
                }
            } else {
                updatePreference(preference, preference.getKey());
            }
        }
    }

    @Override
    public void onSharedPreferenceChanged(SharedPreferences sharedPreferences, String key) {
        updatePreference(findPreference(key), key);
    }

    private void updatePreference(Preference preference, String key) {
        if (preference == null) return;
        if (preference instanceof ListPreference) {
            ListPreference listPreference = (ListPreference) preference;
            listPreference.setSummary(listPreference.getEntry());
            return;
        } else if(preference instanceof EditTextPreference) {
            EditTextPreference editTextPreference = (EditTextPreference) preference;
            editTextPreference.setSummary(editTextPreference.getText());
        }

        SharedPreferences sharedPrefs = getPreferenceManager().getSharedPreferences();
        preference.setSummary(sharedPrefs.getString(key, "Default"));
    }


}
