import { Component } from '@angular/core';

@Component({
  selector: 'app-filters',
  templateUrl: './filters.component.html',
  styleUrls: ['./filters.component.css']
})
export class FiltersComponent {
  selectedState: string;
  selectedRegions: string[] = [];
  selectedDate: Date;
  showForecast: boolean = true;

  applyFilters(): void {
    console.log("Filters applied:", {
      state: this.selectedState,
      regions: this.selectedRegions,
      date: this.selectedDate,
      forecast: this.showForecast
    });
  }
}
