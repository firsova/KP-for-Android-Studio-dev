package petrsu.smartroom.android.srmic;

import android.os.Bundle;
import android.preference.PreferenceFragment;

/**
 * 
 * @author pavlin
 *
 *	Displays application settings
 */
public class SettingsFragment extends PreferenceFragment {

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		addPreferencesFromResource(R.xml.settings);
	}
}
