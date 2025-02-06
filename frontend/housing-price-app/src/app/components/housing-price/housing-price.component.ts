import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Chart, registerables } from 'chart.js';

@Component({
  selector: 'app-housing-price',
  templateUrl: './housing-price.component.html',
  styleUrls: ['./housing-price.component.css']
})
export class HousingPriceComponent implements OnInit {
  priceChart: any;
  forecastChart: any;
  priceData: any = {};
  forecastData: any = {};
  showForecast: boolean = true;

  constructor(private apiService: ApiService) {
    Chart.register(...registerables);
  }

  ngOnInit(): void {
    this.loadPriceTrend();
  }

  loadPriceTrend(): void {
    this.apiService.getPriceTrend().subscribe(data => {
      this.priceData = data;
      this.renderPriceChart();
    });

    if (this.showForecast) {
      this.apiService.getForecast(5).subscribe(data => {
        this.forecastData = data;
        this.renderForecastChart();
      });
    }
  }

  renderPriceChart(): void {
    const ctx = document.getElementById('priceChart') as HTMLCanvasElement;
    if (this.priceChart) this.priceChart.destroy();
    this.priceChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: Object.keys(this.priceData),
        datasets: [{
          label: 'Housing Price Trend',
          data: Object.values(this.priceData),
          borderColor: 'blue',
          borderWidth: 2,
          fill: false
        }]
      }
    });
  }

  renderForecastChart(): void {
    const ctx = document.getElementById('forecastChart') as HTMLCanvasElement;
    if (this.forecastChart) this.forecastChart.destroy();
    this.forecastChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: Object.keys(this.forecastData),
        datasets: [{
          label: 'Forecast (Next 5 months)',
          data: Object.values(this.forecastData),
          borderColor: 'red',
          borderWidth: 2,
          fill: false
        }]
      }
    });
  }
}
