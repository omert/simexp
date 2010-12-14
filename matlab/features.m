function features(x)

f = -ones(26, 1);
f(['b' 'd' 'f' 'h' 'k' 'l' 't']-'a'+1) = 1;
fit_feature(x, f, 2, 'tall / short');
f = -ones(26, 1);
f(['a' 'b' 'c' 'd' 'e' 'g' 'o' 'p' 'q' 's']-'a'+1) = 1;
fit_feature(x, f, 3, 'round / not');
f = -ones(26, 1);
f(['a' 'e' 'i' 'o' 'u']-'a'+1) = 1;
fit_feature(x, f, 4, 'vowels / consonents');
f = randn(26,1);
fit_feature(x, f, 5, 'random');
f = (1:26)';
fit_feature(x, f, 6, 'alphabet');

