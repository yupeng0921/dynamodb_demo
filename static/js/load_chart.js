$(function () {
		$(document).ready(function() {
				Highcharts.setOptions({
					global: {
						useUTC: false
								}
					});

				var chart;
				$('#reader_concurrent').highcharts({
					chart: {
						type: 'spline',
								animation: Highcharts.svg, // don't animate in old IE
								marginRight: 10,
								events: {
							load: function() {
									var url = "reader_concurrent_number";
									var series = this.series[0];
									setInterval(function() {
											// set up the updating of the chart each second
											$.getJSON (url, function (jd) {
													var x = (new Date()).getTime(), // current time
														y = jd.value;
													series.addPoint([x, y], true, true);
												});
										}, 1000);
								}
							}
						},
							title: {
						text: 'concurrent read'
								},
							xAxis: {
						type: 'datetime',
								tickPixelInterval: 150
								},
							yAxis: {
						min: 0,
								max: 2000,
						title: {
							text: 'Value'
									},
								plotLines: [{
								value: 0,
										width: 1,
										color: '#808080'
										}]
								},
							tooltip: {
						formatter: function() {
								                        return '<b>'+ this.series.name +'</b><br/>'+
															Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
															Highcharts.numberFormat(this.y, 2);
							}
						},
							legend: {
						enabled: false
								},
							exporting: {
						enabled: false
								},
							series: [{
							name: 'concurrent read',
									data: (function() {
											// generate an array of random data
											var data = [],
												time = (new Date()).getTime(),
												i;

											for (i = -29; i <= 0; i++) {
												data.push({
													x: time + i * 1000,
															y: 0
															});
											}
											return data;
										})()
									}]
							});
			});

	});

$(function () {
		$(document).ready(function() {
				Highcharts.setOptions({
					global: {
						useUTC: false
								}
					});

				var chart;
				$('#reader_latency').highcharts({
					chart: {
						type: 'spline',
								animation: Highcharts.svg, // don't animate in old IE
								marginRight: 10,
								events: {
							load: function() {
									var url = "reader_latency";
									var series = this.series[0];
									setInterval(function() {
											// set up the updating of the chart each second
											$.getJSON (url, function (jd) {
													var x = (new Date()).getTime(), // current time
														y = jd.value;
													series.addPoint([x, y], true, true);
												});
										}, 1000);
								}
							}
						},
							title: {
						text: 'read latency'
								},
							xAxis: {
						type: 'datetime',
								tickPixelInterval: 150
								},
							yAxis: {
						min: 0,
								max: 100,
						title: {
							text: 'Value'
									},
								plotLines: [{
								value: 0,
										width: 1,
										color: '#808080'
										}]
								},
							tooltip: {
						formatter: function() {
								                        return '<b>'+ this.series.name +'</b><br/>'+
															Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
															Highcharts.numberFormat(this.y, 2);
							}
						},
							legend: {
						enabled: false
								},
							exporting: {
						enabled: false
								},
							series: [{
							name: 'concurrent read',
									data: (function() {
											// generate an array of random data
											var data = [],
												time = (new Date()).getTime(),
												i;

											for (i = -29; i <= 0; i++) {
												data.push({
													x: time + i * 1000,
															y: 0
															});
											}
											return data;
										})()
									}]
							});
			});

	});

$(document).ready(function(){
		$("form#reader_form").submit(function(e){
				e.preventDefault();
				$.ajax({
					url: "/?action=download",
							type: 'post',
							data: $("#reader_form").serialize(),
					});
			});
	});

$(document).ready(function(){
		$("form#writer_form").submit(function(e){
				e.preventDefault();
				$.ajax({
					url: "/?action=upload",
							type: 'post',
							data: $("#writer_form").serialize(),
					});
			});
	});
