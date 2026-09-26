from django.urls import path
from . import views

urlpatterns = [
    # Navigation Views
    path('', views.dashboard_view, name='dashboard'),
    path('notes/', views.notes_view, name='notes'),
    path('goals/', views.goals_view, name='goals'),
    path('settings/', views.settings_view, name='settings'),

    # Task & Subtask Actions
    path('toggle-subtask/<int:subtask_id>/', views.toggle_subtask, name='toggle_subtask'),
    path('delete-subtask/<int:subtask_id>/', views.delete_subtask, name='delete_subtask'),
    path('add-subtask/<int:task_id>/', views.add_subtask, name='add_subtask'),
    path('replace-task/<int:task_id>/', views.replace_task, name='replace_task'),
    path('add-custom-task/', views.add_custom_task, name='add_custom_task'),

    # Lore Dump (Notes) Actions
    path('add-note/', views.add_note, name='add_note'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),

    # The Vision (Goals) Actions
    path('add-goal/', views.add_goal, name='add_goal'),
    path('delete-goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),

    # Control Center Actions
    path('clear-completed/', views.clear_completed_tasks, name='clear_completed'),
    path('reset-data/', views.reset_all_data, name='reset_data'),
]