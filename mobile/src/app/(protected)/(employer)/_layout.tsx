import { NativeTabs } from "expo-router/native-tabs";

export default function EmployerLayout() {
  return (
    <NativeTabs tintColor="#155BC7" backgroundColor="#FFFFFF">
      <NativeTabs.Trigger name="index">
        <NativeTabs.Trigger.Label>Home</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="house.fill" drawable="ic_menu_view" />
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="shifts">
        <NativeTabs.Trigger.Label>Shifts</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="calendar" drawable="ic_menu_today" />
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="workers">
        <NativeTabs.Trigger.Label>Workers</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="person.2.fill" drawable="ic_menu_myplaces" />
      </NativeTabs.Trigger>

      <NativeTabs.Trigger name="settings">
        <NativeTabs.Trigger.Label>Settings</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="gearshape.fill" drawable="ic_menu_manage" />
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}