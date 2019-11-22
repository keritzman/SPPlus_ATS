create view covers_vw as
select a.id, case when home_points+line > away_points then 'home' when home_points+line = away_points then 'push' else 'road' end as covering_team from games a inner join lines b on a.id=b.id


create view sp_results_vw as
select id,sp_line,sp_pick,result from (select *, case when covering_team='push' then 'push' when sp_pick='nopick' then 'nopick'  when covering_team=sp_pick then 'win' else 'loss' end as result from (
		select *, case when line > sp_line then 'home' when line = sp_line then 'nopick' else 'away' end as sp_pick from (
			select a.id,b.week,a.hometeam, a.awayTeam, a.line,b.home_points,b.away_points, c.covering_team,home.rating as home_team_rating, away.rating as away_team_rating, away.rating - home.rating - (case when neutral_site = 0 then 2.5 else 0 end) as sp_line
			from lines a inner join games b on a.id = b.id  --where b.week=13
						inner join weekly_sp home on b.week = home.week and b.home_team = home.team
						inner join weekly_sp away on b.week = away.week and b.away_team = away.team
						inner join covers_vw c on b.id = c.id
			)
		)
	)
