import { Routes } from '@angular/router';
import { MainLayout } from './layout/main-layout/main-layout';

export const routes: Routes = [
  {
    path: '',
    component: MainLayout,
    children: [
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      },
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/dashboard/dashboard')
            .then(m => m.Dashboard)
      },
      {
        path: 'ai-chat',
        loadComponent: () =>
          import('./features/ai-chat/ai-chat')
            .then(m => m.AiChat)
      },
      {
        path: 'inventory',
        loadComponent: () =>
          import('./features/inventory/inventory')
            .then(m => m.Inventory)
      },
      {
        path: 'orders',
        loadComponent: () =>
          import('./features/orders/orders')
            .then(m => m.Orders)
      },
      {
        path: 'knowledge',
        loadComponent: () =>
          import('./features/knowledge/knowledge')
            .then(m => m.Knowledge)
      },
      {
        path: 'evaluation',
        loadComponent: () =>
          import('./features/evaluation/evaluation')
            .then(m => m.Evaluation)
      }
    ]
  },
  {
    path: '**',
    redirectTo: 'dashboard'
  }
];
