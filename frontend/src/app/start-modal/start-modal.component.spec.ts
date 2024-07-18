import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StartModalComponent } from './start-modal.component';

describe('StartModalComponent', () => {
  let component: StartModalComponent;
  let fixture: ComponentFixture<StartModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StartModalComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StartModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
