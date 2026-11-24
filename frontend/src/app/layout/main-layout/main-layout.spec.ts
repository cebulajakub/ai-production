import {
  ComponentFixture,
  TestBed
} from '@angular/core/testing';

import { provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';

import { MainLayout } from './main-layout';
import { Health } from '../../core/services/health';

describe('MainLayout', () => {

  let component: MainLayout;
  let fixture: ComponentFixture<MainLayout>;

  const healthMock = {
    checkHealth: vi.fn()
  };

  beforeEach(async () => {

    healthMock.checkHealth.mockReset();

    healthMock.checkHealth.mockReturnValue(
      of({ status: 'ok' })
    );

    await TestBed.configureTestingModule({
      imports: [MainLayout],
      providers: [
        provideRouter([]),
        {
          provide: Health,
          useValue: healthMock
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(MainLayout);
    component = fixture.componentInstance;

  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should report API online', () => {

    fixture.detectChanges();

    expect(component.apiStatus()).toBe('online');

    expect(
      healthMock.checkHealth
    ).toHaveBeenCalledTimes(1);
  });

  it('should report API offline on error', () => {

    healthMock.checkHealth.mockReturnValue(
      throwError(() => new Error('API unavailable'))
    );

    fixture.detectChanges();

    expect(component.apiStatus()).toBe('offline');
  });

  it('should recover after API becomes available', () => {

    healthMock.checkHealth.mockReturnValue(
      throwError(() => new Error('API unavailable'))
    );

    fixture.detectChanges();

    expect(component.apiStatus()).toBe('offline');

    healthMock.checkHealth.mockReturnValue(
      of({ status: 'ok' })
    );

    component.checkApiHealth();

    expect(component.apiStatus()).toBe('online');
  });

});
